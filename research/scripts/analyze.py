#!/usr/bin/env python3
"""Reproduce descriptive statistics from the frozen, sanitized audit export.

Python 3 standard library only. No network, product installation or credentials.
Run from any directory: python3 scripts/analyze.py
"""
from pathlib import Path
import collections as C
import csv
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
OUT = ROOT / 'results'
EXCLUDED = {'not_applicable', 'per_share_withheld', 'formula_blank_by_design'}

def run():
    OUT.mkdir(exist_ok=True)
    stock_source = {r['symbol']: r for r in csv.DictReader((DATA/'original-by-stock.csv').open())}
    source_rows = list(csv.DictReader((DATA/'original-by-row.csv').open()))
    symbols = {}
    keys = set()
    counts, bystock, rawrows = C.defaultdict(C.Counter), C.defaultdict(C.Counter), C.defaultdict(C.Counter)
    reasons, exclusions, fields = C.Counter(), C.Counter(), C.Counter()
    candidates = C.defaultdict(list)
    total = duplicate_keys = invalid = missing_cik = 0
    with gzip.open(DATA/'row-observations.csv.gz', 'rt', newline='') as f:
        for r in csv.DictReader(f):
            total += 1
            key = (r['symbol'], r['basis'], r['statement'], r['metric'])
            duplicate_keys += key in keys
            keys.add(key)
            invalid += r['status'] not in {'filled', 'gappy', 'hidden'}
            symbols[r['symbol']] = {k:r[k] for k in ['cik','name','tier','archetype']}
            rk = (r['tier'], r['statement'], r['basis'], r['metric'], r['role'])
            rawrows[rk][r['status']] += 1
            rawrows[rk]['total'] += 1
            if r['reason']: rawrows[rk]['reason:'+r['reason']] += 1
            excluded = r['reason'] in EXCLUDED
            assert excluded == (r['excluded_by_original_rule'] == 'true')
            if excluded:
                exclusions[(r['basis'],r['reason'])] += 1
                continue
            for tier in [r['tier'], 'all']:
                counts[(tier,r['basis'],r['statement'])][r['status']] += 1
                counts[(tier,r['basis'],'all')][r['status']] += 1
            bystock[(r['symbol'],r['basis'],r['statement'])][r['status']] += 1
            if r['reason']: reasons[(r['basis'],r['reason'])] += 1
            if r['basis'] != 'annual': continue
            group = None
            if r['status']=='filled': group='filled'
            elif r['reason']=='sec_has_mapped_tag': group='mapped_tag_gap'
            elif r['reason']=='sec_has_alt_tag': group='alternative_tag_gap'
            elif r['status']=='gappy': group='partial'
            elif r['status']=='hidden' and r['reason'] in {'not_reported','unmapped_not_reported','no_statement_rows','no_sec_file'}:
                group='apparent_missing'
            if group:candidates[group].append(r)

    # Reconcile two independent original exports against the detailed records.
    stock_mismatches=[]
    assert set(stock_source)==set(symbols)
    for symbol,s in stock_source.items():
        for statement in ['income','balance','cash']:
            c=bystock[(symbol,'annual',statement)]
            for field,value in [('filled',c['filled']),('gappy',c['gappy']),('rows',sum(c.values()))]:
                if int(s[statement+'_'+field])!=value:stock_mismatches.append([symbol,statement,field])
        q=[bystock[(symbol,'quarterly',st)] for st in ['income','balance','cash']]
        if int(s['quarterly_filled'])!=sum(c['filled'] for c in q) or int(s['quarterly_rows'])!=sum(sum(c.values()) for c in q):
            stock_mismatches.append([symbol,'quarterly'])
    row_mismatches=[]
    for r in source_rows:
        key=tuple(r[k] for k in ['tier','statement','basis','row','role'])
        got=rawrows[key]
        if any(int(r[k])!=got[k] for k in ['filled','gappy','hidden']) or int(r['stocks'])!=got['total']:
            row_mismatches.append(list(key))
        expected=dict(x.rsplit(':',1) for x in r['not_filled_by_reason'].split())
        if {k:int(v) for k,v in expected.items()} != {k[7:]:v for k,v in got.items() if k.startswith('reason:')}:
            row_mismatches.append(list(key)+['reasons'])
    assert not duplicate_keys and not invalid and not stock_mismatches and not row_mismatches

    issuer_symbols=C.defaultdict(list)
    for symbol,v in symbols.items():issuer_symbols[v['cik'] or 'missing:'+symbol].append(symbol)
    canonical={min(v) for v in issuer_symbols.values()}
    canonical_counts=C.defaultdict(C.Counter)
    for (symbol,basis,statement),c in bystock.items():
        if symbol in canonical:canonical_counts[(basis,statement)].update(c)
    coverage=[]
    for (tier,basis,statement),c in sorted(counts.items()):
        n=sum(c.values())
        coverage.append(dict(tier=tier,basis=basis,statement=statement,denominator=n,filled=c['filled'],partial=c['gappy'],missing=c['hidden'],filled_pct=round(100*c['filled']/n,4),partial_pct=round(100*c['gappy']/n,4),missing_pct=round(100*c['hidden']/n,4)))
    with (OUT/'coverage.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(coverage[0]));w.writeheader();w.writerows(coverage)
    selection=[]
    for group in ['filled','partial','mapped_tag_gap','alternative_tag_gap','apparent_missing']:
        seen=set();n=0
        for r in sorted(candidates[group],key=lambda r:(r['symbol'],r['metric'],r['statement'])):
            identity=r['cik'] or r['symbol']
            if identity in seen:continue
            seen.add(identity);n+=1
            selection.append(dict(case_id=f'{group}-{n:02d}',stratum=group,**r))
            if n==6:break
        assert n==6
    with (OUT/'selected-cases.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(selection[0]));w.writeheader();w.writerows(selection)
    annual=sum((canonical_counts[('annual',s)] for s in ['income','balance','cash']),C.Counter())
    summary=dict(snapshot_generated_at='2026-10-25T14:20:34.063Z',frozen_date='2026-10-26',unit='security × statement × basis × presentation row; not individual financial facts',securities=len(symbols),tiers=dict(C.Counter(v['tier'] for v in symbols.values())),distinct_known_ciks=len({v['cik'] for v in symbols.values() if v['cik']}),securities_without_cik=sum(not v['cik'] for v in symbols.values()),multiple_security_ciks=sum(len(v)>1 for k,v in issuer_symbols.items() if not k.startswith('missing:')),securities_in_multiple_security_ciks=sum(len(v) for k,v in issuer_symbols.items() if len(v)>1 and not k.startswith('missing:')),extra_securities_over_canonical=sum(len(v)-1 for v in issuer_symbols.values()),raw_row_observations=total,duplicate_observation_keys=duplicate_keys,by_stock_mismatches=stock_mismatches,by_row_mismatches=row_mismatches,exclusions=[dict(basis=b,reason=r,count=n) for (b,r),n in sorted(exclusions.items())],reasons=[dict(basis=b,reason=r,count=n) for (b,r),n in sorted(reasons.items())],canonical_issuer_sensitivity=dict(selection='lexicographically first ticker per CIK; missing CIKs separate',securities=len(canonical),annual_counts=dict(annual),annual_filled_pct=round(100*annual['filled']/sum(annual.values()),4)),coverage=coverage)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (OUT/'issuer-duplicates.json').write_text(json.dumps({k:sorted(v) for k,v in sorted(issuer_symbols.items()) if len(v)>1},indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['coverage','reasons','exclusions']},indent=2))
    print('Annual overall:',next(r for r in coverage if r['tier']=='all' and r['basis']=='annual' and r['statement']=='all'))
    print('All source-export reconciliation checks passed.')
    return summary

if __name__=='__main__':run()
