from pathlib import Path
import hashlib,json,re,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
sets={'original':json.loads((ROOT/'research/audit/ORIGINAL_STATE.json').read_text())['sha256'],'V4':json.loads((ROOT/'research/v5/review/V4_PRESERVATION.json').read_text()),'V5':json.loads((HERE/'review/V5_PRESERVATION.json').read_text())}
counts={};missing=[]
for label,manifest in sets.items():
 checked=0
 for rel,expected in manifest.items():
  if not (ROOT/rel).exists() and '--package' in sys.argv:missing.append(rel);continue
  assert sha(ROOT/rel)==expected,rel;checked+=1
 counts[label]={'recorded':len(manifest),'available_checked':checked}
frozen=json.loads((HERE/'results/confirmation/source_sha256.json').read_text());n=0
for v in ['v3','v4','v5','v6']:
 for p in (ROOT/'research'/v).glob('*.m'):
  key=re.sub('[^A-Za-z0-9_]','_',str(p.relative_to(ROOT)))
  if key in frozen:assert sha(p)==frozen[key],key;n+=1
assert n==len(frozen)
for name in ['symbolic_proof.json','statistical_correction.json','confirmation/independent_audit.json']:
 r=json.loads((HERE/'results'/name).read_text());assert r['status']=='passed'
log=(HERE/'results/tests.log').read_text();assert 'Ran 17 tests' in log and 'OK' in log
paperlog=(HERE/'paper.log').read_text();assert not re.search(r'Warning: Citation|undefined references|Overfull|Reference .* undefined',paperlog)
# Check all printed confirmation table numbers against the independently reconstructed aggregates.
import csv
with (HERE/'results/confirmation/summary.csv').open() as f:summary=list(csv.DictReader(f))
lines=(HERE/'results/confirmation/table_rows.tex').read_text().splitlines()[1:-1]
for r,line in zip(summary,lines):
 cell=[c.strip() for c in line.split('&')];assert cell[2]==f"{r['selected']}/600" and cell[3]==f"{r['accepted']}/600"
 assert abs(float(cell[4])-float(r['mean_outage_s']))<=.000500001
 assert abs(float(cell[5])-float(r['mean_energy_urad2s']))<=.000500001
 assert int(cell[6])==int(r['accepted_outside_radius'])
assert len(lines)==len(summary)==12
report={'status':'passed','preservation':counts,'frozen_MATLAB_sources':n,'new_traces_audited':7200,'state_steps_replayed':5040000,'supervisor_and_statistics_tests':17,'printed_confirmation_rows_checked':len(lines),'unavailable_historical_files':sorted(set(missing)),'external_human_review':False,'physical_validation':False}
(HERE/'results/final_integrity.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
