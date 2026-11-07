"""Package the executed research, with separate full raw traces and SHA-256 manifests."""
from pathlib import Path
import hashlib,json,zipfile,shutil
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
(OUT/'pdf').mkdir(exist_ok=True)
shutil.copy2(ROOT/'research/v4/paper.pdf',OUT/'pdf/Optical_Fault_Diagnosis_V4_Research_Paper.pdf')
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
raw=[]; code=[]
for folder in ['research','matlab','configs','simulink','revisions/v2','tests']:
    for p in (ROOT/folder).rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(ROOT)
        if any(x in rel.parts for x in ['tmp','__pycache__']): continue
        if p.suffix in ['.autosave','.slxc','.original']: continue
        if p.parent==ROOT/'research/v4/results/final' and p.suffix=='.mat' and p.name.startswith(('primary_','sensitivity_','counterfactual_')):
            raw.append(p);continue
        if folder=='revisions/v2' and 'results' in rel.parts: continue
        if str(rel).startswith('research/v3/results/smoke'): continue
        code.append(p)
for name in ['setup_project.m','start_v2.m','start_research_v3.m','start_research_v4.m','README.md']:
    p=ROOT/name
    if p.exists():code.append(p)
readme='''OPTICAL DIAGNOSIS RESEARCH V4 — EXECUTED SIMULATION STUDY
Extract both ZIP archives into the same folder, preserving paths.
Start with research/v4/README.md and research/audit/FINAL_REVIEW.md.
Paper: research/v4/paper.pdf. Editable source: research/v4/paper.tex.
Reproduction: research/reproducibility/REPRODUCIBILITY.md.
The raw archive contains full MATLAB traces and passive-reference masks.
SHA-256 manifests cover every shipped file. MATLAB is required for simulations.
Status: partially complete against the Transactions research request.
Novelty priority, physical validation, matched published full-system baselines,
source-rights confirmation, and independent external review remain unresolved.
No submission, public release, hardware result, or universal superiority claimed.
Historical private reference extracts and rendering intermediates are omitted.
'''
results={}
for kind,files,name in [('code',code,'Satellite_Optical_Research_V4_Code_and_Reports.zip'),('raw',raw,'Satellite_Optical_Research_V4_Raw_Data.zip')]:
    files=sorted(set(files));manifest={str(p.relative_to(ROOT)):digest(p) for p in files}
    dest=OUT/name
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
        z.writestr('READ_ME_FIRST.txt',readme)
        z.writestr('PACKAGE_SHA256.json' if kind=='code' else 'RAW_DATA_SHA256.json',json.dumps(manifest,indent=2)+'\n')
        for i,p in enumerate(files):
            z.write(p,p.relative_to(ROOT))
            if (i+1)%20==0:print(kind,i+1,'/',len(files),flush=True)
    with zipfile.ZipFile(dest) as z:
        for rel,expected in manifest.items():
            h=hashlib.sha256()
            with z.open(rel) as f:
                for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
            assert h.hexdigest()==expected,rel
    results[kind]={'file':name,'files':len(files),'uncompressed_bytes':sum(p.stat().st_size for p in files),'archive_bytes':dest.stat().st_size,'sha256':digest(dest),'verified':'all archived payload SHA-256 hashes matched'}
    print(kind,'complete',results[kind],flush=True)
(OUT/'V4_DELIVERY_MANIFEST.json').write_text(json.dumps(results,indent=2)+'\n')
print('All archives verified.',flush=True)
