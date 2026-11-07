"""Review revision source/report and full raw supplementary delivery."""
from pathlib import Path
import zipfile,json,hashlib,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OUT=ROOT/'output'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
source=[];raw=[]
for p in HERE.rglob('*'):
 if not p.is_file() or any(k in p.parts for k in ['tmp','__pycache__']):continue
 if p.suffix=='.mat' and p.name.startswith(('trial_','grid_')):raw.append(p)
 else:source.append(p)
source.append(ROOT/'start_research_v5.m')
code=OUT/'Satellite_Optical_Research_V5_Code_and_Reports.zip'
with zipfile.ZipFile(OUT/'Satellite_Optical_Research_V4_Code_and_Reports.zip') as old,zipfile.ZipFile(code,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 manifest={}
 for x in old.infolist():
  if x.filename in ['PACKAGE_SHA256.json','READ_ME_FIRST.txt']:continue
  b=old.read(x.filename);z.writestr(x.filename,b);manifest[x.filename]=hashlib.sha256(b).hexdigest()
 for p in source:
  rel=str(p.relative_to(ROOT));z.write(p,rel);manifest[rel]=sha(p)
 z.writestr('PACKAGE_SHA256.json',json.dumps(manifest,indent=2)+'\n')
 z.writestr('READ_ME_FIRST.txt','V5 submission-review revision. Read research/v5/README.md and review/REVIEW_RESPONSE.md. Extract the V5 raw archive into the same folder. Full historical V4 trace verification also requires the preserved V4 Raw Data archive from the research-v4-2026-10-23 GitHub release. V4 files remain preserved. External human review and physical validation are absent.\n')
 print('Source/report archive complete',code.stat().st_size,flush=True)
rawfile=OUT/'Satellite_Optical_Research_V5_Raw_Data.zip';manifest={str(p.relative_to(ROOT)):sha(p) for p in raw}
with zipfile.ZipFile(rawfile,'w',zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
 z.writestr('V5_RAW_SHA256.json',json.dumps(manifest,indent=2)+'\n')
 for i,p in enumerate(sorted(raw)):
  z.write(p,p.relative_to(ROOT))
  if (i+1)%20==0:print('V5 raw',i+1,'/',len(raw),flush=True)
for archive in [code,rawfile]:
 with zipfile.ZipFile(archive) as z:assert z.testzip() is None
shutil.copy2(HERE/'paper.pdf',OUT/'pdf/Optical_Fault_Diagnosis_V5_Reviewed_Paper.pdf')
report={p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in [code,rawfile,OUT/'pdf/Optical_Fault_Diagnosis_V5_Reviewed_Paper.pdf']}
(OUT/'V5_DELIVERY_MANIFEST.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
