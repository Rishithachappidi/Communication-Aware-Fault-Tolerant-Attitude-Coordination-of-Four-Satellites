"""Separate Python checks of complete traces and vectorized actuator-step replay."""
from pathlib import Path
import sys,json,csv,math
from collections import defaultdict
import numpy as np
from scipy.io import loadmat
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT/'research/v5'))
from independent_checks import check_trace
from analyze_v5 import convert
from supervisor import Evidence,REQUIRED,authorize,monitor
from statistics_tools import family_percentiles
FOLDER=HERE/'results/confirmation'

def replay(z,c):
 X=z['state_history'];Z=z['standardized_noise'];r=z['reference_history'];h=c['dt'];noise=c['noise'];bias=np.array(c['sensorBias']);J0=c['J'];d=c['b'];Ja=J0*c['actualJfactor'];tau=c['tau']*c['actualTaufactor']
 def slope(x):
  q=x[:,:2];v=x[:,2:4];a=x[:,4:6];I=x[:,6:];e=q+bias+noise*Z[:,:2]-r;vm=v+2*noise*Z[:,2:4]
  raw=-J0*c['kp']*e+(d-J0*c['kd'])*vm-J0*c['ki']*I;cmd=np.clip(raw,-c['umax'],c['umax']);dv=(a-d*v)/Ja
  dv=np.where((np.abs(v)>=c['rateMax'])&(np.sign(v)*dv>0),0,dv);di=np.where(np.abs(raw)>c['umax'],0,e)
  return np.column_stack((np.clip(v,-c['rateMax'],c['rateMax']),dv,(cmd-a)/tau,di)),cmd
 k1,cmd=slope(X);k2,_=slope(X+h*k1/2);k3,_=slope(X+h*k2/2);k4,_=slope(X+h*k3)
 pred=X+h*(k1+2*k2+2*k3+k4)/6;truth=np.vstack((X[1:],np.asarray(z['terminal_state']).reshape(1,8)))
 error=float(np.max(np.abs(pred-truth)));np.testing.assert_allclose(pred,truth,rtol=1e-11,atol=2e-17);np.testing.assert_allclose(cmd,z['command'],rtol=1e-11,atol=2e-17)
 np.testing.assert_allclose(X[:,:2],z['angle'],atol=1e-18)
 return error

def save_csv(path,rows):
 with path.open('w') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)

def main():
 with (FOLDER/'trials.csv').open() as f:rows=list(csv.DictReader(f))
 groups=defaultdict(list);P=json.loads((FOLDER/'protocol.json').read_text());methods=P['methods'];seeds=P['seeds']
 for row in rows:groups[f"trace_{row['case_id']}_J{float(row['Jfactor']):g}_T{float(row['taufactor']):g}.mat"].append(row)
 maxerr=0.;steps=0;shadow=0;monitored=0;breaches=0;rebuilt=[]
 for file,records in groups.items():
  a=loadmat(FOLDER/file,simplify_cells=True);c=a['c'];traces=a['traces'];pas=a['passiveTraces']
  for row in records:
   i=seeds.index(int(float(row['seed'])));j=methods.index(row['method']);z=convert(traces[i,j]);p=convert(pas[i]);m=check_trace(z,c,row,p['down'],True);maxerr=max(maxerr,replay(z,c));steps+=len(z['t'])
   if row['method']=='UAD':
    if not m['has']:category='no-probe'
    else:category='within-premise' if m['premises'] else 'out-of-model'
   else:category='not-a-certificate' if m['has'] else 'no-probe'
   row['certificate_category']=category;row['independent_bound_violation']=m['violation'];row['lower_calculated']=m['has'];row['gain_estimate_error']=math.nan
   fit=z['fit']
   if isinstance(fit,dict) and float(row['accepted']):row['gain_estimate_error']=abs(float(fit['gain'])-c['nearGain'])
   if m['has']:
    mask=np.isfinite(z['lower']);ptrue=z['power'][mask];lo=z['lower'][mask];row['median_bound_slack_ratio']=float(np.median((ptrue-lo)/c['sensitivity']));row['min_bound_slack_ratio']=float(np.min((ptrue-lo)/c['sensitivity']))
   else:row['median_bound_slack_ratio']=math.nan;row['min_bound_slack_ratio']=math.nan
   if row['method']=='UAD' and m['has']:
    first=np.flatnonzero(z['probe'])[0];plan=z['plan'];e=Evidence((float(c['actualJfactor']),float(c['actualTaufactor'])),{k:'declared-simulation-contract' for k in REQUIRED},valid_until=100.,relative_power_sigma=float(c['powerNoise']))
    permission=authorize(np.asarray(plan['lower']).ravel().tolist(),float(c['dt']),8*float(plan['dwell']),float(z['measured_power'][first]),float(c['sensitivity']),e)
    assert permission['permission']=='conditional-probe';shadow+=1
    for pm,pb in zip(z['measured_power'][mask],z['lower'][mask]):
     status=monitor(float(pm),float(pb),permission['measurement_eta']);monitored+=1;breaches+=int(status['event']=='bound-breach')
   rebuilt.append(row)
  print('Complete-record replay',file,len(rebuilt),flush=True)
 groups=defaultdict(list)
 for r in rebuilt:groups[(r['case_id'],r['method'])].append(r)
 summary=[];pairs=[];rng=np.random.default_rng(17027)
 for (case,method),rr in groups.items():
  def arr(k):return np.array([float(r[k]) for r in rr])
  x={'case_id':case,'method':method,'n':len(rr),'attempted':int(arr('attempted').sum()),'selected':int(arr('probe_count').sum()),'accepted':int(arr('accepted').sum()),'abstained':int(arr('abstained').sum()),'fit_rejected':int(arr('fit_rejected').sum()),'mean_outage_s':float(arr('outage_s').mean()),'mean_energy_urad2s':float(arr('energy_urad2s').mean()),'false_acquisition':int(arr('false_acquisition').sum()),'bound_violations':int(arr('bound_violation').sum()),'within_premise':sum(r['certificate_category']=='within-premise' for r in rr),'out_of_model':sum(r['certificate_category']=='out-of-model' for r in rr),'unverified':sum(r['certificate_category']=='unverified' for r in rr),'not_a_certificate':sum(r['certificate_category']=='not-a-certificate' for r in rr),'accepted_outside_radius':int(sum(float(r['accepted']) and float(r['coverage_all_fits'])==0 for r in rr)),'mean_plan_ms':float(arr('plan_runtime_s').mean()*1000)}
  for name,key in [('median_trace_median_bound_slack_ratio','median_bound_slack_ratio'),('median_accepted_gain_error','gain_estimate_error')]:
   aa=arr(key);x[name]=float(np.nanmedian(aa)) if np.isfinite(aa).any() else math.nan
  summary.append(x)
  if method=='UAD':
   a={(int(float(r['seed'])),float(r['Jfactor']),float(r['taufactor'])):r for r in rr};b={(int(float(r['seed'])),float(r['Jfactor']),float(r['taufactor'])):r for r in groups[(case,'guarded')]}
   # Seed is the unit; average six fixed actual-model contrasts before resampling.
   differences=[]
   for seed in seeds:differences.append(np.mean([float(a[(seed,j,t)]['accepted'])-float(b[(seed,j,t)]['accepted']) for j in P['J'] for t in P['tau']]))
   d=np.array(differences);bootstrap=d[rng.integers(0,len(seeds),(5000,len(seeds)))].mean(axis=1);ci=np.quantile(bootstrap,[.025,.975]);family=np.quantile(bootstrap,family_percentiles(families=6));pairs.append({'case_id':case,'seed_units':len(seeds),'fixed_models_per_seed':6,'UAD_minus_guard_acceptance':float(d.mean()),'CI95_low':float(ci[0]),'CI95_high':float(ci[1]),'family6_low':float(family[0]),'family6_high':float(family[1])})
 save_csv(FOLDER/'independent_rows.csv',rebuilt);save_csv(FOLDER/'summary.csv',summary);save_csv(FOLDER/'paired.csv',pairs)
 report={'status':'passed','traces':len(rebuilt),'actuator_steps_replayed':steps,'maximum_absolute_state_step_error':maxerr,'conditional_authorizations_shadow_checked':shadow,'measurement_monitor_samples':monitored,'observed_monitor_breaches':breaches,'scope':'Separate NumPy implementation replays held-input RK4 including stage torque/rate clamps and anti-windup from every recorded state/reference/noise history. Supervisor exercised in shadow mode with declared simulation evidence only; no hardware authorization or diagnosis guarantee.'}
 (FOLDER/'independent_audit.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
if __name__=='__main__':main()
