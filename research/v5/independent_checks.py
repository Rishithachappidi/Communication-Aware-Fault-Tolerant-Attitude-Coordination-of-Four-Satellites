"""Independent Python algebra, probability, and saved-record checks.
No imports/calls to MATLAB simulator, evaluator, truth or analysis functions.
V4 missing offset histories are reconstructed from the documented injection protocol;
V5 directly logs offsets and every standardized disturbance for this audit.
"""
from pathlib import Path
import json,csv,math,hashlib
import numpy as np
import h5py
from scipy.io import loadmat
from scipy.special import ndtri
from scipy.optimize import minimize_scalar
from scipy.stats import beta
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OUT=HERE/'results'/'verification';OUT.mkdir(exist_ok=True)
def dump(name,x): (OUT/name).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def scalar(x): return float(np.asarray(x).squeeze())
def read(g,k):
 x=g[k]
 if isinstance(x,h5py.Group):return x
 a=x[...].T
 if x.attrs.get('MATLAB_class',b'')==b'char':return ''.join(chr(int(v)) for v in a.ravel())
 if x.attrs.get('MATLAB_empty',0):return None
 return a.squeeze() if a.size==1 or a.ndim==2 and 1 in a.shape else a

def algebra():
 rng=np.random.default_rng(17023);worst=-math.inf;sharp=0.;cases=0
 # Optimize only direction of d; maximizing e is analytic. Units here are urad.
 for i in range(1200):
  center=rng.normal(size=2)*rng.uniform(0,30);d=rng.normal(size=2)*rng.uniform(0,12)
  R=rng.uniform(0,35);r=rng.uniform(0,5)
  if i%8==0:center*=0
  if i%11==0:d*=0
  if i%13==0:r=0
  if i%17==0:R=0
  bound=2*center@d+2*R*np.linalg.norm(d)+d@d+2*(np.linalg.norm(center+d)+R)*r+r*r
  def f(t):
   x=d+r*np.array([np.cos(t),np.sin(t)])
   return 2*center@x+2*R*np.linalg.norm(x)+x@x
  angles=np.linspace(0,2*np.pi,2049);values=np.array([f(t) for t in angles]);j=int(values.argmax());h=angles[1]
  z=minimize_scalar(lambda t:-f(t),bounds=(angles[j]-h,angles[j]+h),method='bounded',options={'xatol':1e-12})
  maximum=max(values[j],-z.fun);worst=max(worst,maximum-bound);assert maximum<=bound+1e-7
  if np.linalg.norm(center)==0:sharp=max(sharp,abs(maximum-bound));assert abs(maximum-bound)<1e-6
  # Direct optical ratio including negative loss and uncertain divergence.
  for _ in range(8):
   v=rng.normal(size=2);v=v/max(np.linalg.norm(v),1e-100)*r*rng.random();u=rng.normal(size=2);u=u/max(np.linalg.norm(u),1e-100)*R*rng.random()
   e=(center+u)*1e-6;actual=(d+v)*1e-6;alpha=rng.uniform(18,26)*1e-6;t=rng.uniform(0,4);gain=math.exp(-.15*t+rng.uniform(0,.5))
   relative=gain*math.exp(-2*(2*e@actual+actual@actual)/alpha**2)
   lower=math.exp(-.15*t-2*max(bound,0)/18**2)
   assert relative+1e-12>=lower
   # radians / microradians must give identical dimensionless exponents.
   assert abs(2*(bound*1e-12)/(18e-6)**2-2*bound/18**2)<1e-10
  cases+=1
 result={'status':'passed','boundary_optimizations':cases,'direct_power_checks':cases*8,'maximum_excess_urad2':worst,'maximum_centered_sharpness_error_urad2':sharp,'scope':'Independent numerical boundary optimization supports the written analytic proof; not a formal proof assistant or external human review.'};dump('algebra.json',result);return result

def probability():
 rng=np.random.default_rng(17024);N=700;delta=.01;k=ndtri(1-delta/(10*N));tail=math.erfc(k/math.sqrt(2));missions=10000;bad=0;false=0;clipped=0;pointwise_false=0
 for batch in range(20):
  Z=rng.standard_normal((500,N,5));inside=np.max(np.abs(Z),axis=(1,2))<=k;bad+=int((~inside).sum())
  # A deliberately most-adverse selected time (minimum measured power) is
  # stronger than a causal trigger test; exact algorithm triggers are audited below.
  sigma=.08;truth=1.00001;pm=np.maximum(0,truth*(1+sigma*Z[:,:,4]));eta=k*sigma
  chosen=pm.argmin(axis=1);upper=pm[np.arange(500),chosen]/(1-eta)
  false+=int((upper<1).sum());pointwise_false+=int((pm.min(axis=1)/(1-2.576*sigma)<1).sum());clipped+=int((pm==0).sum())
  assert not np.any((upper<1)&inside)
 # On E, eta<1 implies 1+sigma Z>0, hence clipping inactive for p>0;
 # at p=0, pm=0 and [0,0] is valid. eta>=1 must abstain, not divide.
 upper_cp=float(beta.ppf(.95,bad+1,missions-bad))
 out={'status':'passed','N':N,'channels':5,'delta':delta,'kappa':k,'union_tail':5*N*tail,'missions':missions,'event_failures':bad,'event_failure_CP95_upper':upper_cp,'adversarial_selected_time_false_acquisitions':false,'pointwise_99pct_selected_time_false_acquisitions':pointwise_false,'clipped_samples':clipped,'scope':'Uniform-event proof covers arbitrary selection; this adversarial minimum test is not the plant algorithm. Its exact adaptive decisions are separately audited in saved traces. Gaussian scales/tails are assumptions, not hardware calibration.'}
 assert abs(out['union_tail']-delta)<1e-10;dump('probability.json',out);return out

def truth(t,name,seed,c):
 # Reimplementation of documented protocol, no MATLAB function calls.
 b=np.zeros((len(t),2));active=t>=2;angle=.4+.9*math.sin(seed);offset=(20+6*math.cos(seed))*1e-6*np.array([math.cos(angle),math.sin(angle)])*c['offsetScale']
 if name in ['pointing','linear_drift','quadratic_drift','fast_fading','deep_loss']:b[active]=offset
 g=np.ones(len(t));age=t[active]-2
 if name in ['linear_drift','attenuation_only']:g[active]=np.exp(-c['driftSlope']*age)
 elif name=='quadratic_drift':g[active]=np.exp(-c['curvature']*age**2)
 elif name=='fast_fading':g[active]=np.exp(-.045*age+c['fadingAmplitude']*np.sin(4*age))
 elif name=='deep_loss':g[active]=.18
 elif name=='near_threshold':g[active]=c['nearGain']
 elif name=='dark':g[active]=0
 return b,g

def check_trace(z,c,row,passive,v5=False):
 def val(k):return z[k] if v5 else read(z,k)
 t=np.asarray(val('t')).ravel();p=np.asarray(val('power')).ravel();q=np.asarray(val('angle'));qm=np.asarray(val('measured_angle'));pm=np.asarray(val('measured_power')).ravel();probe=np.asarray(val('probe')).ravel().astype(bool);lower=np.asarray(val('lower')).ravel();tube=np.asarray(val('tube')).ravel();motion=np.asarray(val('motion'));dt=c['dt'];mask=t>=2;has=np.isfinite(lower)
 seed=int(float(row['seed']));name=row['scenario'];b,g=truth(t,name,seed,c)
 if v5:
  np.testing.assert_allclose(val('offset_truth'),b,atol=1e-18);np.testing.assert_allclose(val('standardized_noise')[:,:2]*c['noise']+q+np.asarray(c['sensorBias']),qm,atol=1e-18)
  np.testing.assert_allclose(pm,np.maximum(0,p*(1+c['powerNoise']*val('standardized_noise')[:,4])),rtol=1e-12,atol=1e-18)
  assert abs(float(val('noise_max'))-np.abs(val('standardized_noise')).max())<1e-12
 np.testing.assert_allclose(np.asarray(val('gain_truth')).ravel(),g,atol=1e-13)
 alpha=c['alpha']*c['actualAlphaFactor'];p0=c['Pt']*c['eta']*(-np.expm1(-2*(c['aperture']/2)**2/(c['distance']*alpha)**2))
 expected=p0*g*np.exp(-2*np.sum((q+b)**2,axis=1)/alpha**2)
 np.testing.assert_allclose(p,expected,rtol=2e-10,atol=1e-18)
 down=p<c['sensitivity'];passive=np.asarray(passive).ravel().astype(bool)
 def same(k,x,tol=1e-8):
  y=float(row[k]);assert abs(y-x)<tol or np.isnan(x) and np.isnan(y),(k,y,x,name,seed,row['method'])
 same('outage_s',np.sum(down&mask)*dt);same('probe_s',probe.sum()*dt);same('energy_urad2s',np.sum(q[probe]**2)*dt*1e12)
 same('false_correction',int(np.linalg.norm(b[-1])==0 and np.linalg.norm(val('correction'))>c['offsetThreshold']));same('missed_pointing_diagnosis',int(np.linalg.norm(b[-1])>c['offsetThreshold'] and not float(row['accepted'])));same('missed_diagnosis',int((np.linalg.norm(b[-1])>0 or abs(g[-1]-1)>1e-10) and not float(row['accepted'])));same('abstained',int(bool(float(row['attempted'])) and not probe.any()));same('fit_rejected',int(bool(probe.any()) and not float(row['accepted']) and row['method'] not in ['lockin','lockin_native']));same('tail_availability',np.mean(~down[t>=12]));same('probe_induced_outage_s',np.sum(down[mask]&~passive[mask])*dt);same('avoided_outage_s',np.sum(~down[mask]&passive[mask])*dt)
 bv=bool(np.any(p[has]+1e-14<lower[has]));same('bound_violation',int(bv));prem=False;tv=False;constant=False
 if has.any():
  ix=np.flatnonzero(probe);first=ix[0];q0=q[first];tv=bool(np.any(np.linalg.norm(q[has]-q0-motion[has],axis=1)>tube[has]+1e-12));same('tube_violation',int(tv))
  constant=bool(np.all(np.linalg.norm(b[probe]-b[first],axis=1)<1e-15));gainok=bool(np.all(g[probe]>=g[first]*np.exp(-c['driftBound']*(t[probe]-t[first]))-1e-12))
  member=any(abs(c['actualJfactor']-x)<1e-10 for x in np.atleast_1d(c['Jfactors'])) and any(abs(c['actualTaufactor']-x)<1e-10 for x in np.atleast_1d(c['taufactors']))
  prem=constant and gainok and member and c['alphaRange'][0]<=alpha<=c['alphaRange'][1] and g[first]<=c['gainMax'] and np.linalg.norm(b[-1])<=c['priorRadius'] and np.linalg.norm(c['sensorBias'])==0 and float(val('noise_max'))<=c['kappa']
  same('certificate_premises',int(prem))
  lo=pm[first]/(1+c['kappa']*c['powerNoise']);ang=math.sqrt(2)*c['kappa']*c['noise']
  if row['method']=='UAD_point_gate':lo=pm[first]
  R=min(c['priorRadius']+np.linalg.norm(qm[first])+ang,c['alphaRange'][1]*math.sqrt(max(0,math.log(c['p0Range'][1]*c['gainMax']/max(lo,np.finfo(float).tiny)))/2))
  dnorm=np.linalg.norm(motion[has],axis=1);ss=dnorm+tube[has];D=2*R*ss+ss**2
  fresh=lo*np.exp(-c['driftBound']*(t[has]-t[first])-2*D/c['alphaRange'][0]**2)
  np.testing.assert_allclose(lower[has],fresh,rtol=1e-11,atol=1e-20)
 if probe.any():
  first=np.flatnonzero(probe)[0];same('false_acquisition',int(row['mode']=='acquisition' and p[first]>=c['sensitivity']))
  if row['method'] in ['UAD','guarded']:
   eta=c['kappa']*c['powerNoise'];hi=pm[first]/(1-eta) if eta<1 else math.inf
   mode='acquisition' if hi<c['sensitivity'] else ('service' if pm[first]/(1+eta)>=c['sensitivity'] else 'uncertain')
   assert mode==row['mode']
 # Independently reconstruct the exact three-consecutive residual trigger.
 anomaly=np.abs(np.log(np.maximum(pm,.0001*c['p0'])/np.maximum(c['p0']*np.exp(-2*np.sum(qm**2,axis=1)/c['alpha']**2),.0001*c['p0'])))>c['detectLog']
 count=0;trigger=None
 for i in range(len(t)):
  count=count+1 if t[i]>1 and anomaly[i] else 0
  if count>=c['detectionCount']:trigger=i;break
 if row['method']!='passive':same('attempted',int(trigger is not None))
 if probe.any():assert np.flatnonzero(probe)[0]==trigger
 fit=val('fit');fit=fit if isinstance(fit,(dict,h5py.Group)) else None
 if fit is not None:
  fb=np.asarray(fit['b'] if v5 else read(fit,'b')).ravel();fr=scalar(fit['radius'] if v5 else read(fit,'radius'));ok=scalar(fit['ok'] if v5 else read(fit,'ok'));same('accepted',ok)
  if np.all(np.isfinite(fb)):
   err=np.linalg.norm(fb-b[-1])*1e6
   if ok:same('accepted_error_um',err)
   same('coverage_all_fits',int(np.linalg.norm(fb-b[-1])<=fr))
 return {'has':int(has.any()),'premises':int(prem),'violation':int(bv),'valid_violation':int(prem and bv),'tube_violation':int(tv),'constant':int(constant),'outage':float(np.sum(down&mask)*dt)}

def raw_v4():
 folder=ROOT/'research/v4/results/final';protocol=json.loads((folder/'protocol.json').read_text());rows=[]
 for name in ['primary_corrected.csv','sensitivity_corrected.csv']:
  with (folder/name).open() as f:rows+=list(csv.DictReader(f))
 groups={}
 for row in rows:
  if row['condition']=='primary':file='primary_'+row['scenario']+'.mat';methods=protocol['methods'];seeds=protocol['primarySeeds']
  else:
   value=float(row['condition_value']);file=f"sensitivity_{row['condition']}_{value:g}_{row['scenario']}.mat";s=next(x for x in protocol['sweeps'] if x['name']==row['condition']);methods=s['methods'];seeds=protocol['sensitivitySeeds']
  groups.setdefault(file,[]).append((row,methods.index(row['method']),seeds.index(int(float(row['seed'])))))
 total=0;summary={};stats={'selected':0,'valid':0,'invalid':0,'violations_valid':0,'violations_invalid':0};rebuilt=[]
 for filename,entries in groups.items():
  with h5py.File(folder/filename) as f:
   c={k:read(f['c'],k) for k in f['c']};counter=None
   if filename.startswith('sensitivity_'):counter=loadmat(folder/('counterfactual_'+filename))['passiveDown']
   for row,j,i in entries:
    z=f[f['traces'][j,i]];pas=read(f[f['traces'][0,i]],'down') if counter is None else counter[:,i]
    m=check_trace(z,c,row,pas);total+=1
    key=(row['condition'],row['scenario'],row['method'],row['condition_value']);x=summary.setdefault(key,{'n':0,'outage':0.,'accepted':0,'premises':0,'violations':0,'outages':[],'energies':[],'errors':[]});x['outages'].append(m['outage']);x['energies'].append(float(row['energy_urad2s']));x['errors']+=([float(row['accepted_error_um'])] if float(row['accepted']) else []);x['n']+=1;x['outage']+=m['outage'];x['accepted']+=int(float(row['accepted']));x['premises']+=m['premises'];x['violations']+=m['violation']
    rebuilt.append({'condition':row['condition'],'condition_value':row['condition_value'],'scenario':row['scenario'],'method':row['method'],'seed':row['seed'],**m})
    if row['method']=='UAD' and m['has']:
     stats['selected']+=1;stats['valid']+=m['premises'];stats['invalid']+=1-m['premises'];stats['violations_valid']+=m['valid_violation'];stats['violations_invalid']+=m['violation']-m['valid_violation']
  print('Independent raw check',filename,total,flush=True)
 # Check every V4 primary printed table row against independent per-trace aggregates.
 table=(folder/'primary_rows.tex').read_text();checked=0
 for (condition,scenario,method,value),x in summary.items():
  if condition!='primary' or method not in ['projected_fixed','parameter_kf','DAP','UAD']:continue
  printed=next(line for line in table.splitlines() if line.startswith(scenario.replace('_',' ')+' & '+method.replace('_',' ')+' &'))
  cells=printed.split('&');assert cells[2].strip()==f"{x['accepted']}/{x['n']}";assert abs(float(cells[4])-x['outage']/x['n'])<=.000500001;assert abs(float(cells[5])-np.quantile(x['outages'],.95))<=.000500001;assert abs(float(cells[6].strip().split()[0])-np.mean(x['energies']))<=.00500001
  if x['errors']:assert abs(float(cells[3])-np.median(x['errors']))<=.000500001
  else:assert cells[3].strip()=='--'
  checked+=1
 with (OUT/'v4_reconstructed.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=rebuilt[0]);w.writeheader();w.writerows(rebuilt)
 out={'status':'passed','traces':total,'mat_chunks':len(groups),'printed_primary_rows_checked':checked,'UAD_all_primary_and_sensitivity':stats,'scope':'Separate Python implementation. V4 offset histories absent: reconstructed from documented frozen injection formula, not independently measured. Rate disturbances absent: global noise_max relies on recorded scalar; V5 logs every disturbance. No physical or external human replication.'};dump('v4_raw.json',out);return out

if __name__=='__main__':
 import sys
 task=sys.argv[1] if len(sys.argv)>1 else 'all'
 if task in ['all','algebra']:print(algebra(),flush=True)
 if task in ['all','probability']:print(probability(),flush=True)
 if task in ['all','v4']:print(raw_v4(),flush=True)
