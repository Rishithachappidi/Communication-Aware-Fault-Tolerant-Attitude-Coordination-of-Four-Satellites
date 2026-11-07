"""Resume release uploads and verify GitHub's SHA-256 digests against the manifest."""
import concurrent.futures, datetime, json, os, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parent
REPO = 'kaushalrog/Satellite-Optical-Fault-Recovery'
TAG = 'research-v7-2026-10-23'
def release():
    return json.loads(subprocess.check_output(['gh','api',f'repos/{REPO}/releases/tags/{TAG}']))
def upload(part):
    path = ROOT/'V7_Raw_Release_Parts'/part['name']
    for attempt in range(4):
        result = subprocess.run(['gh','release','upload',TAG,str(path),'--repo',REPO,'--clobber'],env={**os.environ,'GODEBUG':'http2client=0'},capture_output=True,text=True,timeout=330)
        if result.returncode == 0:
            print('Uploaded', part['name'], flush=True)
            return
    raise RuntimeError(result.stderr)
def main():
    manifest = json.loads((ROOT/'V7_RAW_DATA_CHUNKS.json').read_text())
    parts = [p for a in manifest['archives'] for p in a['parts']]
    existing = {a['name']: a for a in release()['assets']}
    missing = [p for p in parts if p['name'] not in existing or existing[p['name']]['size'] != p['bytes'] or existing[p['name']].get('digest') != 'sha256:'+p['sha256']]
    print('Remaining uploads:',len(missing),flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(upload, missing))
    existing = {a['name']:a for a in release()['assets']}
    for p in parts:
        assert existing[p['name']]['size'] == p['bytes'], p['name']
        assert existing[p['name']]['digest'] == 'sha256:'+p['sha256'], p['name']
    result={'status':'verified','verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repository':REPO,'tag':TAG,'parts_verified':len(parts),'archives':[{'name':a['name'],'bytes':a['bytes'],'sha256':a['sha256'],'parts':len(a['parts'])} for a in manifest['archives']]}
    path=ROOT/'V7_RAW_PUBLICATION_MANIFEST.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'V7_RAW_UPLOAD_STATUS.json').write_text(json.dumps(result,indent=2)+'\n')
    subprocess.run(['gh','release','upload',TAG,str(path),'--repo',REPO,'--clobber'],check=True)
    print('Verified all',len(parts),'parts',flush=True)
if __name__=='__main__':main()
