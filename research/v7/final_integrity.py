from pathlib import Path
import hashlib,json,re,csv,sys
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
sets={'original':json.loads((ROOT/'research/audit/ORIGINAL_STATE.json').read_text())['sha256'],'V4':json.loads((ROOT/'research/v5/review/V4_PRESERVATION.json').read_text()),'V5':json.loads((ROOT/'research/v6/review/V5_PRESERVATION.json').read_text()),'V6':json.loads((H/'review/V6_PRESERVATION.json').read_text())};counts={};missing=[]
for label,manifest in sets.items():
 checked=0
 for rel,expected in manifest.items():
  if not (ROOT/rel).exists() and '--package' in sys.argv:missing.append(rel);continue
  assert sha(ROOT/rel)==expected,rel;checked+=1
 counts[label]=dict(recorded=len(manifest),checked=checked)
frozen=json.loads((H/'results/matched_baselines/source_sha256.json').read_text());checked=0
for v in ['v3','v4','v5','v6','v7']:
 for p in (ROOT/'research'/v).glob('*.m'):
  key=re.sub('[^A-Za-z0-9_]','_',str(p.relative_to(ROOT)))
  if key in frozen:assert sha(p)==frozen[key],key;checked+=1
assert checked==len(frozen)
for name in ['measurement_units.json','baseline_audit.json','symbolic_proof.json','shadow_audit.json']:assert json.loads((H/'results'/name).read_text())['status']=='passed'
log=(H/'results/tests.log').read_text();assert 'Ran 22 tests' in log and 'OK' in log
for name in ['paper','supplement']:
 log=(H/f'{name}.log').read_text();assert not re.search(r'Warning: Citation|undefined references|Overfull|Reference .* undefined',log),name
with (H/'results/matched_summary.csv').open() as f:summary=list(csv.DictReader(f))
lines=(H/'results/matched_rows.tex').read_text().splitlines()[1:-1];assert len(summary)==len(lines)==24
for r,line in zip(summary,lines):
 cells=[x.strip() for x in line.split('&')];assert int(cells[2])==int(r['selected']);assert cells[3]==('--' if r['method']=='lockin' else r['accepted']);assert cells[4]==('--' if r['method']=='lockin' else r['confidence_misses']);assert int(cells[5])==int(r['incomplete_probes']);assert abs(float(cells[6])-float(r['mean_outage_s']))<.00050001;assert abs(float(cells[7].replace('\\',''))-float(r['mean_energy_urad2s']))<.00050001
assert sum(int(r['n']) for r in summary)==14400
raw=list((H/'results/matched_baselines').glob('trace_*.mat'));assert len(raw)==36
report=dict(status='passed',preservation=counts,frozen_MATLAB_sources=checked,printed_matched_rows_checked=24,new_traces=7200,combined_matched_records=14400,new_steps_replayed=5040000,combined_steps_replayed=10080000,tests=22,new_trace_chunks=len(raw),missing_historical_files=missing,physical_validation=False,external_human_review=False)
(H/'results/final_integrity.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
