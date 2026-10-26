#!/usr/bin/env python3
"""Check analytical invariants and the rendered paper; no source-system writes."""
from pathlib import Path
import collections,csv,json,re
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]

def main():
    s=json.loads((ROOT/'results/summary.json').read_text())
    for r in s['coverage']:
        assert r['filled']+r['partial']+r['missing']==r['denominator']
        for name in ['filled','partial','missing']:
            assert abs(100*r[name]/r['denominator']-r[name+'_pct'])<.00006
    annual=next(r for r in s['coverage'] if (r['tier'],r['basis'],r['statement'])==('all','annual','all'))
    assert sum(r['count'] for r in s['reasons'] if r['basis']=='annual')==annual['partial']+annual['missing']
    assert annual['denominator']+sum(r['count'] for r in s['exclusions'] if r['basis']=='annual')==s['raw_row_observations']//2
    assert s['distinct_known_ciks']+s['securities_without_cik']+s['extra_securities_over_canonical']==s['securities']
    selected=list(csv.DictReader((ROOT/'results/selected-cases.csv').open()))
    reviewed=list(csv.DictReader((ROOT/'data/case-review.csv').open()))
    assert len(selected)==len(reviewed)==30
    assert set(collections.Counter(r['stratum'] for r in reviewed).values())=={6}
    index={r['case_id']:r for r in selected}
    for c in reviewed:
        r=index[c['case_id']]
        assert (r['symbol'],r['statement'],r['metric'],r['status'])==(c['symbol'],c['statement'],c['metric'],c['snapshot_status'])
    assert len({(r['symbol'],r['statement'],r['metric']) for r in selected})==30
    for group in {r['stratum'] for r in selected}:
        rows=[r for r in selected if r['stratum']==group]
        assert len({r['cik'] or r['symbol'] for r in rows})==6
    periods=json.loads((ROOT/'data/sample-period-values.json').read_text())
    assert all(r['status_matches_frozen'] for r in periods)
    values=[p['value'] for r in periods for p in r['periods']]
    assert None in values and 0 in values
    assert any(len(r['periods'])==1 for r in periods if r['case_id'].startswith('filled-'))
    history=list(csv.DictReader((ROOT/'data/aac-filing-history.csv').open()))
    history_meta=json.loads((ROOT/'data/aac-history-provenance.json').read_text())
    assert history and not history_meta['additional_history_files']
    assert not any(r['form'] in ['10-K','10-K/A','20-F','20-F/A','40-F'] for r in history)
    assert next(r for r in reviewed if r['symbol']=='AAC')['review_status']=='annual_target_unresolved'
    doc=PdfReader(ROOT/'financial-statement-coverage-audit.pdf')
    text='\n'.join(page.extract_text() for page in doc.pages)
    assert all(len(page.extract_text())>250 for page in doc.pages)
    for token in ['394,799','220,665','34,429','139,705','852,416','Avinash Sreekumar','Not peer reviewed','Appendix A','Appendix B']:
        assert token in text,token
    assert all(c['case_id'] in text for c in reviewed)
    assert '\ufffd' not in text
    urls=[]
    for page in doc.pages:
        for a in page.get('/Annots',[]):
            action=a.get_object().get('/A',{})
            if action.get('/URI'):urls.append(str(action['/URI']))
    assert len({u for u in urls if '/Archives/edgar/' in u})==21
    product_links=[u for u in urls if 'stockportfolio.pro/connect' in u]
    assert len(product_links)==1 and 'utm_content=statement_coverage_paper' in product_links[0]
    forbidden=re.compile(r'/home/|/tmp/|mongodb\+srv|sk_live_|sp_live_|@gmail\.com|BEGIN [A-Z ]*PRIVATE KEY',re.I)
    for f in ROOT.rglob('*'):
        if f.is_file() and f.suffix in {'.md','.json','.csv','.ipynb','.txt'}:
            assert not forbidden.search(f.read_text()),f.name
    assert not forbidden.search(text)
    result={'status':'passed','annual_denominator':annual['denominator'],'cases':30,'pdf_pages':len(doc.pages),'distinct_filing_links':21,'pdf_product_links':1,'statistical_invariants':'passed','case_selection':'passed','null_zero_separation':'passed','unresolved_case_retained':'passed','public_artifact_screen':'passed','visual_review':'Recorded separately; not certified by this script.'}
    (ROOT/'results/package-validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
