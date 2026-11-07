from pathlib import Path
import sys,csv,json
import numpy as np
from scipy.io import loadmat
H=Path(__file__).resolve().parent;ROOT=H.parents[1];sys.path.insert(0,str(ROOT/'research/v5'))
from analyze_v5 import convert
from supervisor import Evidence,REQUIRED,authorize,monitor
F=ROOT/'research/v6/results/confirmation';count=0;samples=0;breach=0
for file in sorted(F.glob('trace_*.mat')):
 a=loadmat(file,simplify_cells=True);c=a['c']
 for i in range(100):
  z=convert(a['traces'][i,0]);mask=np.isfinite(z['lower'])
  if not mask.any():continue
  ix=np.flatnonzero(z['probe']);first=ix[0];ev=Evidence((c['actualJfactor'],c['actualTaufactor']),{k:'declared-simulation' for k in REQUIRED},valid_until=14.,relative_power_sigma=c['powerNoise'])
  r=authorize(z['plan']['lower'].ravel().tolist(),c['dt'],8*z['plan']['dwell'],float(z['measured_power'][first]),c['sensitivity'],ev,now=float(z['t'][first]));assert r['permission']=='conditional-probe',r
  count+=1
  for pm,lo in zip(z['measured_power'][mask],z['lower'][mask]):samples+=1;breach+=int(monitor(float(pm),float(lo),r['measurement_eta'])['event']=='bound-breach')
report=dict(status='passed',conditional_authorizations=count,monitor_samples=samples,breaches=breach,scope='V7 remaining-horizon/unit checks replayed on original UAD records with actual mission start; shadow mode only.')
(H/'results/shadow_audit.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
