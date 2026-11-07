"""Transparent statistics-only correction. Never edit preserved V5 sources/results."""
from pathlib import Path
import csv,json
from collections import defaultdict
import numpy as np
from statistics_tools import family_percentiles
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'v5/results/final'
with (OLD/'independently_checked_rows.csv').open() as f:rows=list(csv.DictReader(f))
with (OLD/'paired.csv').open() as f:original={ (r['condition'],r['scenario'],r['comparison']):r for r in csv.DictReader(f)}
groups=defaultdict(list)
for r in rows:groups[(r['condition'],r['scenario'],r['method'])].append(r)
rng=np.random.default_rng(17025);corrected=[];changed=0
for (condition,scenario,method),rr in groups.items():
 if method not in ['DAP','guarded','lockin','lockin_native'] or condition=='continuous_grid':continue
 a={int(float(r['seed'])):float(r['outage_s']) for r in rr};b={int(float(r['seed'])):float(r['outage_s']) for r in groups[(condition,scenario,'UAD')]};keys=sorted(a);diff=np.array([b[k]-a[k] for k in keys]);boots=diff[rng.integers(0,len(keys),(5000,len(keys)))].mean(axis=1)
 ci=np.quantile(boots,[.025,.975]);family=np.quantile(boots,family_percentiles(families=36));old=original[(condition,scenario,'UAD minus '+method)]
 assert abs(float(old['CI95_low'])-ci[0])<1e-12 and abs(float(old['CI95_high'])-ci[1])<1e-12
 assert abs(float(old['family36_low'])-family[0])<1e-12
 r=dict(old);r['family36_high_recorded']=r['family36_high'];r['family36_high']=float(family[1]);changed+=int(abs(float(r['family36_high_recorded'])-family[1])>1e-12)
 assert family[0]<=ci[0]+1e-12 and family[1]>=ci[1]-1e-12
 corrected.append(r)
with (HERE/'results/v5_paired_corrected.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=corrected[0]);w.writeheader();w.writerows(corrected)
report={'status':'passed','contrasts':len(corrected),'changed_adjusted_upper_limits':changed,'defect':'V5 used .975/36 instead of 1-.025/36 for upper Bonferroni percentile.','correction':'alpha/(2m), 1-alpha/(2m), m=36. Existing random bootstrap sequence preserved.','unchanged':'Every per-run outcome, paired mean, descriptive 95% endpoint and adjusted lower endpoint. V4 family9 implementation was correct. V5 original files remain preserved.'}
(HERE/'results/statistical_correction.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
