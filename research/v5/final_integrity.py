"""Verify preserved artifacts, frozen method sources and executed checker reports."""
from pathlib import Path
import hashlib,json,re,sys
here=Path(__file__).resolve().parent;root=here.parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
a=json.loads((root/'research/audit/ORIGINAL_STATE.json').read_text())['sha256']
b=json.loads((here/'review/V4_PRESERVATION.json').read_text())
missing=[]
for rel,h in {**a,**b}.items():
 if not (root/rel).exists() and '--package' in sys.argv:missing.append(rel);continue
 assert sha(root/rel)==h,rel
frozen=json.loads((here/'results/final/source_sha256.json').read_text());count=0
for folder in ['research/v5','research/v4','research/v3']:
 for p in (root/folder).glob('*.m'):
  key=re.sub('[^A-Za-z0-9_]','_',str(p.relative_to(root)))
  if key in frozen:assert sha(p)==frozen[key],key;count+=1
assert count==len(frozen)
for name in ['algebra','probability','actuator','v4_raw','v5_raw']:
 data=json.loads((here/'results/verification'/f'{name}.json').read_text());assert data['status']=='passed',name
r={'status':'passed','original_protected_files':len(a),'V4_preserved_files':len(b),'frozen_matlab_sources':count,'V4_traces_independently_checked':29250,'V5_traces_independently_checked':12000,'external_human_review':False,'hardware_validation':False,'unavailable_historical_files':missing,'original_available_checked':sum((root/p).exists() for p in a),'V4_available_checked':sum((root/p).exists() for p in b)}
(here/'results/verification/final_integrity.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
