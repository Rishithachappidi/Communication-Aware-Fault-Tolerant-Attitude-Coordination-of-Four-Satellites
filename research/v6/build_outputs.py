from pathlib import Path
import csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
H=Path(__file__).resolve().parent;R=H/'results';F=R/'confirmation'
def load(p):
 with p.open() as f:return list(csv.DictReader(f))
summary=load(F/'summary.csv');P=json.loads((F/'protocol.json').read_text());rows=[]
for case in P['cases']:
 for method in ['UAD','guarded']:
  r=next(x for x in summary if x['case_id']==case['id'] and x['method']==method)
  rows.append(f"{case['id'].replace('direction','R').replace('_',' ')} & {'UAD' if method=='UAD' else 'Fixed guard'} & {r['selected']}/600 & {r['accepted']}/600 & {float(r['mean_outage_s']):.3f} & {float(r['mean_energy_urad2s']):.3f} & {r['accepted_outside_radius']} & {float(r['median_trace_median_bound_slack_ratio']):.3f} "+r'\\')
rows=[line.replace('nan', '--') for line in rows]
(F/'table_rows.tex').write_text('\\def\\FrontierRows{\n'+'\n'.join(rows)+'\n}\n')
evidence=load(R/'evidence_totals.csv');rows=[]
for x in evidence:rows.append(f"{x['dataset']} & {x['category']} & {x['probes']} & {x['bound_violations']} "+r'\\')
(R/'evidence_rows.tex').write_text('\\def\\EvidenceRows{\n'+'\n'.join(rows)+'\n}\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(10.5,3.7),constrained_layout=True)
m=load(R/'development/admission_map.csv');m=[r for r in m if float(r['drift_bound'])==0];noise=sorted(set(float(r['noise_scale']) for r in m));power=sorted(set(float(r['power_ratio']) for r in m));grid=np.zeros((len(noise),len(power)))
for r in m:grid[noise.index(float(r['noise_scale'])),power.index(float(r['power_ratio']))]=int(r['UAD_admit'])+2*int(r['guard_admit'])
ax[0].imshow(grid,origin='lower',aspect='auto',extent=[power[0]-.0025,power[-1]+.0025,-.5,len(noise)-.5],interpolation='none',cmap=ListedColormap(['#ededed','#2166ac','#e08214','#762a83']),vmin=0,vmax=3)
ax[0].set_yticks(range(len(noise)),[str(n) for n in noise]);ax[0].set_xlim(1.8,2.205);ax[0].set_xlabel(r'Measured power / sensitivity');ax[0].set_ylabel('Sensor standard-deviation scale');ax[0].set_title('(a) Admission map, gain bound L = 0')
from matplotlib.patches import Patch
ax[0].legend(handles=[Patch(color=c,label=l) for c,l in [('#ededed','Neither'),('#2166ac','UAD only'),('#e08214','Guard only'),('#762a83','Both')]],loc='upper left',fontsize=10.5)
for direction,ns in [(1,.25),(2,.75)]:
 for c in [x for x in P['cases'] if x['direction']==direction]:ax[0].plot(c['power_ratio'],noise.index(ns),'ko',ms=4)
caseids=['direction1_middle','direction2_middle'];x=np.arange(2)
for j,(method,label,color) in enumerate([('UAD','UAD','#2166ac'),('guarded','Fixed guard','#e08214')]):
 vals=[int(next(r['accepted'] for r in summary if r['case_id']==c and r['method']==method))/600*100 for c in caseids]
 ax[1].bar(x+(j-.5)*.3,vals,width=.3,label=label,color=color)
ax[1].set_xticks(x,['Region 1 middle','Region 2 middle']);ax[1].set_ylim(0,105);ax[1].set_ylabel('Accepted parameter fits (%)');ax[1].set_title('(b) Causal confirmation, 100 paired seeds');ax[1].legend(frameon=False);ax[1].grid(axis='y',alpha=.2);ax[1].set_axisbelow(True)
fig.savefig(R/'admission_confirmation.pdf');fig.savefig(R/'admission_confirmation.png',dpi=180)
# Preserve cited original sources; avoid changing V5 bibliography.
s=(H.parent/'v5/references.tex').read_text()
import re
items={}
for part in s.split('\\bibitem{')[1:]:
 key=part.split('}',1)[0];items[key]='\\bibitem{'+part.split('\\end{thebibliography}')[0]
order=[]
for group in re.findall(r'\\cite\{([^}]+)\}',(H/'paper.tex').read_text()):
 for key in group.split(','):
  if key not in order:order.append(key)
assert all(key in items for key in order)
(H/'references.tex').write_text('\\begin{thebibliography}{99}\n'+''.join(items[key] for key in order)+'\\end{thebibliography}\n')
