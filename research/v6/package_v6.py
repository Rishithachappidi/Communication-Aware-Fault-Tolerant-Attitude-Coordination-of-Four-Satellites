"""Versioned local source/report and complete new raw-trace delivery."""
from pathlib import Path
import json,zipfile,hashlib,shutil
H=Path(__file__).resolve().parent;ROOT=H.parents[1];OUT=ROOT/'output'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
source=[];raw=[]
for p in H.rglob('*'):
 if not p.is_file() or any(x in p.parts for x in ['tmp','__pycache__']):continue
 (raw if p.suffix=='.mat' and p.name.startswith('trace_') else source).append(p)
source.append(ROOT/'start_research_v6.m');code=OUT/'Satellite_Optical_Research_V6_Code_and_Reports.zip'
manifest={}
with zipfile.ZipFile(OUT/'Satellite_Optical_Research_V5_Code_and_Reports.zip') as prev,zipfile.ZipFile(code,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for item in prev.infolist():
  if item.filename in ['PACKAGE_SHA256.json','READ_ME_FIRST.txt']:continue
  b=prev.read(item.filename);z.writestr(item.filename,b);manifest[item.filename]=hashlib.sha256(b).hexdigest()
 for p in source:
  rel=str(p.relative_to(ROOT));z.write(p,rel);manifest[rel]=sha(p)
 z.writestr('PACKAGE_SHA256.json',json.dumps(manifest,indent=2)+'\n')
 z.writestr('READ_ME_FIRST.txt','Start with research/v6/README.md and review/REVIEW_RESPONSE.md. V6 is a separate six-page research revision, not a submission-ready claim. Extract V6_Raw_Data.zip at this same root. Older raw-data archives are needed only for full historical reruns/preservation checks. V5 family36 upper intervals contain a disclosed bug: use research/v6/results/v5_paired_corrected.csv. Old exports are preserved.\n')
with zipfile.ZipFile(code) as z:
 for rel,h in manifest.items():assert hashlib.sha256(z.read(rel)).hexdigest()==h
print('V6 source/report payloads verified',len(manifest),code.stat().st_size,flush=True)
dest=OUT/'Satellite_Optical_Research_V6_Raw_Data.zip';manifest={str(p.relative_to(ROOT)):sha(p) for p in raw}
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
 z.writestr('V6_RAW_SHA256.json',json.dumps(manifest,indent=2)+'\n')
 for i,p in enumerate(sorted(raw)):
  z.write(p,p.relative_to(ROOT))
  if (i+1)%6==0:print('V6 raw chunks',i+1,'/',len(raw),flush=True)
with zipfile.ZipFile(dest) as z:
 for rel,h in manifest.items():
  actual=hashlib.sha256()
  with z.open(rel) as f:
   for b in iter(lambda:f.read(1048576),b''):actual.update(b)
  assert actual.hexdigest()==h,rel
pdf=OUT/'pdf/Optical_Fault_Diagnosis_V6_Reviewed_Paper.pdf';shutil.copy2(H/'paper.pdf',pdf)
report={p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in [code,dest,pdf]};(OUT/'V6_DELIVERY_MANIFEST.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
