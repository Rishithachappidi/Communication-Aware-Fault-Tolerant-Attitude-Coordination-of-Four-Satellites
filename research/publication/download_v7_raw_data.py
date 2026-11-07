"""Download/reassemble exact research raw archives from lossless release parts.
Place V7_RAW_DATA_CHUNKS.json alongside this script. Python standard library only.
An existing valid part is reused; interrupted downloads are retried on rerun.
"""
from pathlib import Path
import json,hashlib,urllib.request,time,sys
D=Path(__file__).resolve().parent;M=json.loads((D/'V7_RAW_DATA_CHUNKS.json').read_text());version=sys.argv[1] if len(sys.argv)>1 else '7'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
for a in M['archives']:
 if version!='all' and f'_V{version}_' not in a['name']:continue
 parts=[]
 for c in a['parts']:
  p=D/c['name'];parts.append(p)
  if p.exists() and p.stat().st_size==c['bytes'] and sha(p)==c['sha256']:continue
  for attempt in range(5):
   try:
    with urllib.request.urlopen(c['url'],timeout=120) as source,p.open('wb') as target:
     while block:=source.read(1048576):target.write(block)
    assert p.stat().st_size==c['bytes'] and sha(p)==c['sha256'];break
   except Exception:
    if attempt==4:raise
    time.sleep(5)
  print('Verified',p.name,flush=True)
 dest=D/a['name'];temporary=D/(a['name']+'.assembling')
 with temporary.open('wb') as f:
  for p in parts:
   with p.open('rb') as q:
    while block:=q.read(1048576):f.write(block)
 assert temporary.stat().st_size==a['bytes'] and sha(temporary)==a['sha256']
 temporary.replace(dest);print('Reassembled and verified',dest,flush=True)
print('Extract the selected raw ZIPs at the same root as the V7 code archive. Use argument6 for original confirmation,5 for historical sensitivities, or all for all archives.')
