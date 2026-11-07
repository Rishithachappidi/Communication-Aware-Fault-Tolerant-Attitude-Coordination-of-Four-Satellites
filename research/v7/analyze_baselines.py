"""Independent extension audit; no edits to inherited results."""
from pathlib import Path
import sys,csv,json,math
from collections import defaultdict
import numpy as np
from scipy.io import loadmat
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
sys.path.insert(0,str(ROOT/'research/v6'))
from analyze_confirmation import replay,convert,check_trace,save_csv
from statistics_tools import family_percentiles
from check_trace_v7 import check_trace
F=H/'results/matched_baselines'
def main():
 P=json.loads((F/'protocol.json').read_text());rows=list(csv.DictReader((F/'trials.csv').open()));groups=defaultdict(list)
 for r in rows:groups[f"trace_{r['case_id']}_J{float(r['Jfactor']):g}_T{float(r['taufactor']):g}.mat"].append(r)
 rebuilt=[];mx=0.;steps=0
 for file,rr in groups.items():
  a=loadmat(F/file,simplify_cells=True);c=a['c']
  for r in rr:
   i=P['seeds'].index(int(float(r['seed'])));j=P['methods'].index(r['method']);z=convert(a['traces'][i,j]);pas=convert(a['passiveTraces'][i]);m=check_trace(z,c,r,pas['down'],True)
   mx=max(mx,replay(z,c));steps+=len(z['t'])
   np.testing.assert_allclose(z['measured_rate'],z['state_history'][:,2:4]+c['rateNoise']*z['standardized_noise'][:,2:4],rtol=0,atol=0)
   assert c['rateNoise']==2*c['noise'] and c['rateNoiseUnit']=='rad/s'
   r['certificate_category']='not-a-certificate' if float(r['probe_count']) else 'no-probe';r['independent_bound_violation']=m['violation'];r['lower_calculated']=m['has'];r['median_bound_slack_ratio']=math.nan;r['gain_estimate_error']=math.nan
   if isinstance(z['fit'],dict) and float(r['accepted']):r['gain_estimate_error']=abs(float(z['fit']['gain'])-c['nearGain'])
   rebuilt.append(r)
  print(file,len(rebuilt),flush=True)
 save_csv(F/'independent_rows.csv',rebuilt)
 old=list(csv.DictReader((ROOT/'research/v6/results/confirmation/independent_rows.csv').open()));allrows=old+rebuilt;keys=list(dict.fromkeys(k for r in allrows for k in r))
 with (H/'results/all_matched_rows.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(allrows)
 G=defaultdict(list)
 for r in allrows:G[(r['case_id'],r['method'])].append(r)
 summary=[];paired=[];rng=np.random.default_rng(17028)
 for case in P['cases']:
  for method in ['UAD','guarded','parameter_kf','lockin']:
   rr=G[(case['id'],method)];arr=lambda k:np.array([float(r[k]) for r in rr]);acc=arr('accepted')
   s=dict(case_id=case['id'],method=method,n=len(rr),selected=int(arr('probe_count').sum()),accepted=int(acc.sum()),confidence_misses=int(np.sum(acc*(arr('coverage_all_fits')==0))),incomplete_probes=int(np.sum((arr('probe_count')>0)&~np.isfinite(arr('finish_s')))),mean_outage_s=arr('outage_s').mean(),mean_probe_outage_s=arr('probe_induced_outage_s').mean(),mean_energy_urad2s=arr('energy_urad2s').mean(),mean_plan_ms=1000*arr('plan_runtime_s').mean(),mean_fit_ms=1000*arr('fit_runtime_s').mean())
   slack=arr('median_bound_slack_ratio');s['median_slack_ratio']=float(np.nanmedian(slack)) if np.isfinite(slack).any() else math.nan
   summary.append(s)
  for comparator in ['guarded','parameter_kf','lockin']:
   lookup=lambda mm:{(int(float(r['seed'])),float(r['Jfactor']),float(r['taufactor'])):r for r in G[(case['id'],mm)]}
   aa,bb=lookup('UAD'),lookup(comparator)
   for outcome in ['accepted','energy_urad2s','outage_s']:
    d=np.array([np.mean([float(aa[(seed,j,t)][outcome])-float(bb[(seed,j,t)][outcome]) for j in P['J'] for t in P['tau']]) for seed in P['seeds']]);bs=d[rng.integers(0,len(d),(5000,len(d)))].mean(axis=1);ci=np.quantile(bs,[.025,.975]);fc=np.quantile(bs,family_percentiles(families=6))
    if comparator=='lockin' and outcome=='accepted':continue
    paired.append(dict(case_id=case['id'],comparator=comparator,outcome=outcome,seed_units=100,models_per_seed=6,difference=float(d.mean()),CI95_low=ci[0],CI95_high=ci[1],family6_low=fc[0],family6_high=fc[1],scope='Exploratory family of six settings, separately per comparator and outcome; not simultaneous across all endpoints.'))
 save_csv(H/'results/matched_summary.csv',summary);save_csv(H/'results/matched_paired.csv',paired)
 report=dict(status='passed',new_traces=len(rebuilt),new_actuator_steps=steps,max_state_error=mx,total_matched_traces=len(allrows),scope='New baseline extension independently replayed. Original two-method confirmation independently audited in preserved V6; four methods were not jointly predeclared. No physical replication.')
 (H/'results/baseline_audit.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
if __name__=='__main__':main()
