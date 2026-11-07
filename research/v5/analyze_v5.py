"""Read saved V5 traces and independently reconstruct metrics; summarize paired runs."""
from independent_checks import *
from collections import defaultdict

def convert(x):
 if hasattr(x,'_fieldnames'):return {k:convert(getattr(x,k)) for k in x._fieldnames}
 if isinstance(x,dict):return {k:convert(v) for k,v in x.items()}
 return x

def writecsv(path,rows):
 with path.open('w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)

def main():
 folder=HERE/'results'/'final';p=json.loads((folder/'protocol.json').read_text());allrows=[];audit=[];identical_pairs=0
 for csvname in ['comparisons.csv','actuator_grid.csv','../native/native.csv']:
  with (folder/csvname).open() as f:rows=list(csv.DictReader(f))
  groups=defaultdict(list)
  for row in rows:
   if row['condition']=='continuous_grid':name=f"grid_{float(row['Jfactor']):g}_{float(row['taufactor']):g}_{row['scenario']}.mat";seeds=p['actuatorSeeds'];methods=p['actuatorMethods'];parent=folder
   else:name=f"trial_{row['condition']}_{row['scenario']}.mat";seeds=p['seeds'];methods=['lockin_native'] if 'native' in csvname else p['methods'];parent=folder/'../native' if 'native' in csvname else folder
   groups[parent/name].append((row,seeds.index(int(float(row['seed']))),methods.index(row['method'])))
  for path,entries in groups.items():
   d=loadmat(path,simplify_cells=True);c=d['c'];traces=d['traces'];pas=d['passiveTraces']
   for row,i,j in entries:
    raw=traces[i,j] if len(methods)>1 else traces[i];z=convert(raw);passive=convert(pas[i])['down'];metrics=check_trace(z,c,row,passive,True)
    row['accepted_inaccurate_1um']=int(float(row['accepted']) and float(row['accepted_error_um'])>1)
    row['accepted_outside_radius']=int(float(row['accepted']) and float(row['coverage_all_fits'])==0)
    row['independent_premises']=metrics['premises'];row['independent_valid_violations']=metrics['valid_violation'];allrows.append(row)
   if 'UAD' in methods and 'guarded' in methods:
    for i in range(len(seeds)):
     a=convert(traces[i,methods.index('UAD')]);b=convert(traces[i,methods.index('guarded')])
     assert np.array_equal(a['power'],b['power']) and np.array_equal(a['angle'],b['angle']) and np.array_equal(a['probe'],b['probe'])
     identical_pairs+=1
   print('Independent V5 check',path.name,len(allrows),flush=True)
 groups=defaultdict(list)
 for r in allrows:groups[(r['condition'],r['scenario'],r['method'])].append(r)
 summary=[]
 for (condition,scenario,method),rows in groups.items():
  def v(k):return np.array([float(r[k]) for r in rows])
  n=len(rows);outage=v('outage_s');acc=v('accepted').sum();bound=v('certified_probe').sum();valid=v('independent_premises').sum()
  summary.append({'condition':condition,'scenario':scenario,'method':method,'n':n,'accepted':int(acc),'abstained':int(v('abstained').sum()),'fit_rejected':int(v('fit_rejected').sum()),'missed_diagnosis':int(v('missed_diagnosis').sum()),'false_correction':int(v('false_correction').sum()),'accepted_inaccurate_1um':int(v('accepted_inaccurate_1um').sum()),'accepted_outside_radius':int(v('accepted_outside_radius').sum()),'false_acquisition':int(v('false_acquisition').sum()),'mean_outage_s':outage.mean(),'p95_outage_s':np.quantile(outage,.95),'mean_energy_urad2s':v('energy_urad2s').mean(),'mean_probe_s':v('probe_s').mean(),'bound_calculated':int(bound),'valid_model_flag':int(valid),'invalid_model_flag':int(bound-valid),'bound_violations':int(v('bound_violation').sum()),'valid_model_bound_violations':int(v('independent_valid_violations').sum()),'tube_violations':int(v('tube_violation').sum()),'mean_plan_ms':v('plan_runtime_s').mean()*1000,'p95_plan_ms':np.quantile(v('plan_runtime_s'),.95)*1000})
 pairs=[];rng=np.random.default_rng(17025)
 for (condition,scenario,method),rows in groups.items():
  if method not in ['DAP','guarded','lockin','lockin_native'] or condition=='continuous_grid':continue
  other=groups[(condition,scenario,'UAD')];a={int(float(r['seed'])):float(r['outage_s']) for r in rows};b={int(float(r['seed'])):float(r['outage_s']) for r in other};keys=sorted(a);diff=np.array([b[s]-a[s] for s in keys]);boots=diff[rng.integers(0,len(keys),(5000,len(keys)))].mean(axis=1)
  ci=np.quantile(boots,[.025,.975]);family=np.quantile(boots,[.025/36,.975/36]);pairs.append({'condition':condition,'scenario':scenario,'comparison':'UAD minus '+method,'n':len(keys),'mean_difference_s':diff.mean(),'CI95_low':ci[0],'CI95_high':ci[1],'family36_low':family[0],'family36_high':family[1]})
 writecsv(folder/'summary.csv',summary);writecsv(folder/'paired.csv',pairs);writecsv(folder/'independently_checked_rows.csv',allrows)
 report={'status':'passed','trace_count':len(allrows),'matched_trials':7200,'actuator_trials':3000,'native_trials':1800,'preserved_V4_sha256_files':0,'UAD_guarded_identical_trajectory_pairs':identical_pairs,'scope':'Separate Python raw-trace audit, including recorded offset and every noise channel in V5. Fixed-margin bound/model flags do not confer UAD theorem status.'}
 preserved=json.loads((HERE/'review/V4_PRESERVATION.json').read_text())
 for rel,h in preserved.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel
 report['preserved_V4_sha256_files']=len(preserved);dump('v5_raw.json',report)
 # Manuscript rows: all four scenarios of primary interest, plus fast gain; all methods.
 labels={'DAP':'DAP','UAD':'UAD','guarded':'Fixed margin','lockin':'ES 2.88 s','lockin_native':'ES 8 s'}
 lines=[]
 for condition,scenario in [('nominal','pointing'),('nominal','linear_drift'),('nominal','fast_fading'),('noise5','near_threshold'),('early_fault','pointing')]:
  for method in labels:
   r=next(x for x in summary if x['condition']==condition and x['scenario']==scenario and x['method']==method)
   lines.append(f"{condition.replace('_',' ')} / {scenario.replace('_',' ')} & {labels[method]} & {r['accepted']}/{r['n']} & {r['mean_outage_s']:.3f} & {r['mean_energy_urad2s']:.2f} & {r['false_acquisition']} & {r['bound_violations']} "+r'\\')
 (folder/'review_rows.tex').write_text('\\def\\ReviewRows{\n'+'\n'.join(lines)+'\n}\n')
 macros={'NewTrials':len(allrows),'NewMatched':7200,'NewGrid':3000,'NewNative':1800}
 for key,cond,scenario,method in [('NewDAPDrift','nominal','linear_drift','DAP'),('NewUADDrift','nominal','linear_drift','UAD'),('NewGuardDrift','nominal','linear_drift','guarded'),('NewESDrift','nominal','linear_drift','lockin'),('NewNativeDrift','nominal','linear_drift','lockin_native')]:macros[key]=f"{next(x for x in summary if (x['condition'],x['scenario'],x['method'])==(cond,scenario,method))['mean_outage_s']:.4f}"
 (folder/'review_numbers.tex').write_text('\n'.join('\\newcommand{\\'+k+'}{'+str(v)+'}' for k,v in macros.items())+'\n')
 md=['# V5 executed review-revision results','','12,000 new trials: 7,200 time-matched comparison, 3,000 actuator-grid, 1,800 paired native ES. The native extension was declared after the main outcomes and before its own execution; no settings changed.','','The UAD/guarded/ES 2.88-s cap matches time only, not angular energy. Historical DAP retains its 0.35/0.50-s library; all selected DAP probes in these records last 2.8 s. The frozen descriptor clarification is explicit in protocol_clarification.json. A tracker has no accepted fault diagnosis. Fixed-margin bounds are heuristic and never inherit the proven actuator enclosure.','','|Condition|Scenario|Method|Accepted/n|Abstain|Outage s|P95 s|Energy urad²s|False acquisition|Bound failures|Valid model flag|Inaccurate accepted >1um|','|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
 for r in summary:md.append(f"|{r['condition']}|{r['scenario']}|{r['method']}|{r['accepted']}/{r['n']}|{r['abstained']}|{r['mean_outage_s']:.4f}|{r['p95_outage_s']:.3f}|{r['mean_energy_urad2s']:.3f}|{r['false_acquisition']}|{r['bound_violations']}|{r['valid_model_flag']}|{r['accepted_inaccurate_1um']}|")
 md+=['','All 144 paired contrasts, 95% intervals and approximate family-36 limits are in paired.csv. The 36-family adjustment applies to the scenario/condition family for each comparator, not all comparator families together. Actuator-grid summaries pool 25 prespecified parameter points (20 seeds/point); a pooled 500 is not a homogeneous hardware population. Full per-point records are retained. Error >1um defines an accepted inaccurate offset, not an invented fault-class label. Miscoverage, false correction and missed diagnosis are separate columns. Planner timings are host/JIT-dependent measured online times; neither offline cost nor worst-case embedded timing.']
 (HERE/'review/RESULTS.md').write_text('\n'.join(md)+'\n');print(report)
if __name__=='__main__':main()
