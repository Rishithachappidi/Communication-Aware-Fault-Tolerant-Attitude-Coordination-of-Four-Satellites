from pathlib import Path
import json,hashlib,zipfile,shutil,sys
H=Path(__file__).resolve().parent;ROOT=H.parents[1];OUT=ROOT/'output'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
source=[];raw=[]
for p in H.rglob('*'):
 if not p.is_file() or any(x in p.parts for x in ['tmp','__pycache__']) or p.name=='DELIVERED_SOURCE_SHA256.json':continue
 (raw if p.suffix=='.mat' and p.name.startswith('trace_') else source).append(p)
source.extend([ROOT/'start_research_v7.m',ROOT/'RESEARCH_V7_START_HERE.md'])
manifest={str(p.relative_to(ROOT)):sha(p) for p in source};(H/'results/DELIVERED_SOURCE_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');source.append(H/'results/DELIVERED_SOURCE_SHA256.json')
code=OUT/'Satellite_Optical_Research_V7_Code_and_Reports.zip';payload={}
with zipfile.ZipFile(OUT/'Satellite_Optical_Research_V6_Code_and_Reports.zip') as prev,zipfile.ZipFile(code,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for item in prev.infolist():
  if item.filename in ['PACKAGE_SHA256.json','READ_ME_FIRST.txt']:continue
  b=prev.read(item.filename);z.writestr(item.filename,b);payload[item.filename]=hashlib.sha256(b).hexdigest()
 for p in source:
  rel=str(p.relative_to(ROOT));z.write(p,rel);payload[rel]=sha(p)
 z.writestr('PACKAGE_SHA256.json',json.dumps(payload,indent=2)+'\n')
 z.writestr('READ_ME_FIRST.txt','Start with RESEARCH_V7_START_HERE.md and research/v7/review/REVIEW_RESPONSE.md. V7 is a regular-paper research candidate, not a novelty/physical/submission approval. Extract V7_Raw_Data.zip and V6_Raw_Data.zip at this root for complete combined confirmation analysis. Older raw archives are needed for historical reruns only. V5 statistical upper-tail correction is in research/v6/results/v5_paired_corrected.csv; originals remain preserved.\n')
with zipfile.ZipFile(code) as z:
 for rel,h in payload.items():assert hashlib.sha256(z.read(rel)).hexdigest()==h,rel
print('Code payload verified',len(payload),code.stat().st_size,flush=True)
dest=OUT/'Satellite_Optical_Research_V7_Raw_Data.zip';manifest={str(p.relative_to(ROOT)):sha(p) for p in raw}
if '--code-only' not in sys.argv:
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
  z.writestr('V7_RAW_SHA256.json',json.dumps(manifest,indent=2)+'\n')
  for i,p in enumerate(sorted(raw)):
   z.write(p,p.relative_to(ROOT))
   if (i+1)%6==0:print('Raw chunks',i+1,'/',len(raw),flush=True)
 with zipfile.ZipFile(dest) as z:
  for rel,h in manifest.items():
   actual=hashlib.sha256()
   with z.open(rel) as f:
    for b in iter(lambda:f.read(1048576),b''):actual.update(b)
   assert actual.hexdigest()==h,rel
files=[code,dest]
for src,name in [('paper.pdf','Optical_Fault_Diagnosis_V7_Regular_Paper_Candidate.pdf'),('supplement.pdf','Optical_Fault_Diagnosis_V7_Supplement.pdf')]:
 p=OUT/'pdf'/name;shutil.copy2(H/src,p);files.append(p)
report={p.name:dict(bytes=p.stat().st_size,sha256=sha(p)) for p in files};(OUT/'V7_DELIVERY_MANIFEST.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
