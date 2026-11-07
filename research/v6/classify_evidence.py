"""Three evidence classes for UAD only; do not equate reconstructed flags with full raw evidence."""
from pathlib import Path
import csv,json
from collections import defaultdict
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def load(p):
 with p.open() as f:return list(csv.DictReader(f))
def save(p,rows):
 with p.open('w') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
rows=[]
# Known violated hypotheses take precedence; missing histories prevent a strict
# within-premise label for the otherwise-compatible historical records.
for r in load(ROOT/'research/v5/results/verification/v4_reconstructed.csv'):
 if r['method']!='UAD' or int(r['has'])==0:continue
 valid=int(r['premises']);rows.append({'dataset':'V4','condition':r['condition']+'='+r['condition_value'],'scenario':r['scenario'],'seed':r['seed'],'category':'unverified' if valid else 'out-of-model','bound_violation':r['violation'],'provenance':'documented-protocol reconstruction and summary maximum; full offset/rate-noise histories absent'})
for r in load(ROOT/'research/v5/results/final/independently_checked_rows.csv'):
 if r['method']!='UAD' or float(r['certified_probe'])==0:continue
 rows.append({'dataset':'V5','condition':r['condition'],'scenario':r['scenario'],'seed':r['seed'],'category':'within-premise' if float(r['independent_premises']) else 'out-of-model','bound_violation':r['bound_violation'],'provenance':'complete logged offset and standardized disturbances plus declared simulator model; not physical calibration'})
for r in load(HERE/'results/confirmation/independent_rows.csv'):
 if r['method']!='UAD' or float(r['lower_calculated'])==0:continue
 rows.append({'dataset':'V6','condition':r['case_id'],'scenario':r['scenario'],'seed':r['seed'],'category':r['certificate_category'],'bound_violation':r['bound_violation'],'provenance':'complete states/references/noise/offsets and independent plant-step replay; declared simulation model only'})
groups=defaultdict(list)
for r in rows:groups[(r['dataset'],r['condition'],r['scenario'],r['category'])].append(r)
summary=[]
for key,rr in groups.items():summary.append(dict(zip(['dataset','condition','scenario','category'],key),probes=len(rr),bound_violations=sum(int(float(r['bound_violation'])) for r in rr)))
totals=[]
for dataset in ['V4','V5','V6']:
 for category in ['within-premise','out-of-model','unverified']:
  rr=[r for r in rows if r['dataset']==dataset and r['category']==category];totals.append({'dataset':dataset,'category':category,'probes':len(rr),'bound_violations':sum(int(float(r['bound_violation'])) for r in rr)})
save(HERE/'results/evidence_rows.csv',rows);save(HERE/'results/evidence_by_condition.csv',summary);save(HERE/'results/evidence_totals.csv',totals)
policy={'scope':'UAD probes with a calculated bound only. Non-probing trials reported separately. Fixed-margin calculations are not certified UAD probes.','precedence':['A known failed premise -> out-of-model, even when other evidence is missing.','No known failed premise but missing full required histories -> unverified.','Complete required histories and every numeric premise check passes -> within-premise under the declared simulator model.'],'historical_change':'The 1564 V4 reconstructed-compatible flags are now unverified in this stricter evidence table, not newly verified. Their old labels/results remain preserved.','distribution_assumption':'Within-premise does not mean a Gaussian distribution or physical calibration can be established from a single trace; the simulation generator and declared model remain assumptions. No category is a field reliability population.'}
(HERE/'results/evidence_policy.json').write_text(json.dumps(policy,indent=2)+'\n');print(json.dumps(totals))
