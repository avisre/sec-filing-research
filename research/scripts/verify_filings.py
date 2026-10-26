#!/usr/bin/env python3
"""Verify 27 numeric receipts and three narrative/form checks against SEC originals.

Requires lxml. Full filings are downloaded only to the specified cache, not bundled.
Set SEC_USER_AGENT to an identifying name and contact before online retrieval.
"""
from pathlib import Path
from decimal import Decimal
import argparse, csv, hashlib, json, os, re, time, urllib.request
from lxml import etree

ROOT=Path(__file__).resolve().parents[1]

def check(cache, offline=False):
    refs={r['reference_id']:r for r in csv.DictReader((ROOT/'data/filing-references.csv').open())}
    checks=list(csv.DictReader((ROOT/'data/fact-checks.csv').open()))
    cache.mkdir(parents=True,exist_ok=True)
    trees={};errors=[];passed=[]
    for key,r in refs.items():
        f=cache/(r['stem']+'.html')
        if not f.exists():
            if offline:raise FileNotFoundError(f'Missing cached original: {f}')
            ua=os.environ.get('SEC_USER_AGENT')
            if not ua:raise ValueError('Set SEC_USER_AGENT to your research name and contact.')
            with urllib.request.urlopen(urllib.request.Request(r['url'],headers={'User-Agent':ua}),timeout=40) as response:
                f.write_bytes(response.read())
            time.sleep(.25)
        raw=f.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=r['sha256']:
            errors.append(f'{key}: original-document bytes changed; review before accepting')
        trees[key]=etree.HTML(raw)
    for r in checks:
        t=trees[r['reference_id']]
        matches=t.xpath('//*[@id=$id]',id=r['element_id'])
        assert len(matches)==1,(r['case_id'],'element missing or duplicated')
        e=matches[0];raw=''.join(e.itertext()).strip()
        raw=raw.replace(',','').replace(' ','').replace('−','-').replace('(','').replace(')','')
        if raw in ['—','–','-',''] and 'zero' in e.get('format',''):
            value=Decimal(0)
        else:value=Decimal(raw)*Decimal(10)**int(e.get('scale','0'))*(-1 if e.get('sign')=='-' else 1)
        context=t.xpath('//*[@id=$id]',id=e.get('contextref'))[0]
        dates={str(x.tag).split(':')[-1]:x.text for x in context.iter() if str(x.tag).split(':')[-1] in ['startdate','enddate','instant']}
        dims=[{'axis':x.get('dimension'),'member':x.text} for x in context.iter() if str(x.tag).endswith('explicitmember') or str(x.tag).endswith('typedmember')]
        unit=t.xpath('//*[@id=$id]',id=e.get('unitref'))[0]
        assert e.get('name')==r['tag'],r['case_id']
        assert value==Decimal(r['value']),r['case_id']
        assert (dates.get('enddate') or dates.get('instant') or '')==r['period_end'],r['case_id']
        assert (dates.get('startdate') or '')==r['period_start'],r['case_id']
        assert ' '.join(unit.itertext()).strip()==r['unit'],r['case_id']
        assert dims==json.loads(r['dimensions']),r['case_id']
        passed.append(r['case_id'])
    bystem={r['stem']:trees[k] for k,r in refs.items()}
    def text(stem):return re.sub(r'\s+',' ',' '.join(bystem[stem].itertext()))
    assert re.search(r'no cash dividend payments during the years ended December 31, 2025 and 2024',text('AAL'),re.I)
    assert re.search(r'NOVEMBER 13, 2025.*?DECEMBER 31, 2025',text('AACO'),re.I)
    assert re.search(r'unaudited.*?condensed.*?financial statements',text('AAC'),re.I)
    passed.extend(['partial-03','apparent_missing-03','apparent_missing-06'])
    result={'numeric_checks':27,'narrative_or_reporting_basis_checks':3,'unique_cases':len(set(passed)),'document_checks':len(refs),'document_hash_errors':errors,'caveat':'Passing receipts establish the scoped facts, not full historical accuracy, metric equivalence or a missing-value cause. The AAC annual target remains unresolved.'}
    assert len(set(passed))==30
    if errors:raise AssertionError(errors)
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--cache-dir',type=Path,required=True)
    parser.add_argument('--offline',action='store_true')
    args=parser.parse_args();check(args.cache_dir,args.offline)
