from pathlib import Path
import csv,json,math,sys
import numpy as np
from scipy.io import loadmat
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch,Circle,Patch
H=Path(__file__).resolve().parent;ROOT=H.parents[1];R=H/'results'
sys.path.insert(0,str(ROOT/'research/v5'));from analyze_v5 import convert
load=lambda p:list(csv.DictReader(p.open()))
S=load(R/'matched_summary.csv');P=json.loads((ROOT/'research/v6/results/confirmation/protocol.json').read_text());names={'UAD':'Certificate','guarded':'Fixed guard','parameter_kf':'Parameter KF','lockin':'ES tracker'}
rows=[]
for c in P['cases']:
 for method in names:
  r=next(x for x in S if x['case_id']==c['id'] and x['method']==method)
  rows.append(f"{c['id'].replace('direction','R').replace('_',' ')} & {names[method]} & {r['selected']} & {r['accepted'] if method!='lockin' else '--'} & {r['confidence_misses'] if method!='lockin' else '--'} & {r['incomplete_probes']} & {float(r['mean_outage_s']):.3f} & {float(r['mean_energy_urad2s']):.3f} "+r'\\')
(R/'matched_rows.tex').write_text('\\def\\MatchedRows{\n'+'\n'.join(rows)+'\n}\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
# Explicit guarantee boundaries in information flow.
fig,ax=plt.subplots(figsize=(10.4,3.8));ax.set_xlim(0,10.4);ax.set_ylim(0,3.8);ax.axis('off')
def box(x,y,w,h,label,color):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.04',fc=color,ec='#34495e',lw=.8));ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=11)
def arrow(a,b,label=''):
 ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=11,lw=1,color='#34495e'))
 if label:ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+.12,label,ha='center',fontsize=10.5)
box(.1,2.35,1.6,.8,'Candidate\nplanner','#eaf2f8');box(2.2,2.35,1.6,.8,'Contract\nvalidator','#eaf2f8');box(4.35,2.35,1.75,.8,'Power bound +\noutage budget','#d6eaf8');box(6.65,2.35,1.65,.8,'Authorize /\nrefuse','#d6eaf8');box(8.8,2.35,1.5,.8,'PID +\nterminal','#eaf2f8')
for a,b in [((1.7,2.75),(2.2,2.75)),((3.8,2.75),(4.35,2.75)),((6.1,2.75),(6.65,2.75)),((8.3,2.75),(8.8,2.75))]:arrow(a,b)
box(2.2,.95,1.6,.8,'Model, optics,\nsensor evidence','#fcf3cf');arrow((3,1.75),(3,2.35))
box(6.65,.95,1.65,.8,'Bound monitor\n(shadow mode)','#fcf3cf');arrow((9.55,2.35),(8.3,1.35),'measurements');arrow((7.48,1.75),(7.48,2.35),'breach')
box(8.8,.95,1.5,.8,'Parameter\nestimator','#f5eef8');arrow((9.55,2.35),(9.55,1.75));box(8.8,.08,1.5,.6,'Fault / recovery\ndecision','#f5eef8');arrow((9.55,.95),(9.55,.68))
ax.text(.1,.25,'Blue path: conditional sampled probe service.\nPurple path: separate estimation and recovery; no inherited guarantee.',fontsize=11)
fig.savefig(R/'information_flow.pdf',bbox_inches='tight');plt.close(fig)
# Actual recorded trace, no fabricated experiment.
a=loadmat(ROOT/'research/v6/results/confirmation/trace_direction1_middle_J1_T1.mat',simplify_cells=True);z=convert(a['traces'][0,0]);c=a['c'];ix=np.flatnonzero(z['probe']);first=ix[0];middle=ix[len(ix)//2];j=middle-first;kappa=c['kappa'];eta=kappa*c['powerNoise'];lo=z['measured_power'][first]/(1+eta);ang=math.sqrt(2)*kappa*c['noise'];Rprior=c['priorRadius']+np.linalg.norm(z['measured_angle'][first])+ang;Rpower=c['alphaRange'][1]*math.sqrt(max(0,math.log(c['p0Range'][1]*c['gainMax']/lo))/2);rad=min(Rprior,Rpower);d=z['motion'][middle];rr=z['tube'][middle];actuald=z['angle'][middle]-z['angle'][first]
fig,ax=plt.subplots(1,3,figsize=(10.4,3.0),constrained_layout=True)
for aa,cen,rad0,pt,title in [(ax[0],np.zeros(2),rad,z['angle'][first]+z['offset_truth'][first],'(a) Starting error enclosure'),(ax[1],d,rr,actuald,'(b) Delivered increment enclosure')]:
 aa.add_patch(Circle(cen*1e6,rad0*1e6,fc='#d6eaf8',ec='#2166ac'));aa.plot(*(pt*1e6),'kx',ms=6,label='Recorded truth');aa.plot(*(cen*1e6),'o',ms=3,color='#2166ac');aa.set_aspect('equal');pad=max(rad0*1e6*1.3,.2);aa.set_xlim(cen[0]*1e6-pad,cen[0]*1e6+pad);aa.set_ylim(cen[1]*1e6-pad,cen[1]*1e6+pad);aa.set_xlabel('Axis 1 (µrad)');aa.set_ylabel('Axis 2 (µrad)');aa.set_title(title,fontsize=11)
ax[0].legend(fontsize=10.5,loc='lower right');tt=z['t'][ix]-z['t'][first];ax[2].plot(tt,z['power'][ix]/c['sensitivity'],label='True power',color='#2166ac');ax[2].plot(tt,z['lower'][ix]/c['sensitivity'],label='Lower bound',color='#b2182b');ax[2].axhline(1,color='black',ls='--',label='Sensitivity');ax[2].set_xlabel('Probe age (s)');ax[2].set_ylabel('Power / sensitivity');ax[2].set_title('(c) Sampled service certificate',fontsize=11);ax[2].legend(fontsize=10.5);fig.savefig(R/'certificate_geometry.pdf');plt.close(fig)
(R/'certificate_figure_source.json').write_text(json.dumps(dict(source='research/v6/results/confirmation/trace_direction1_middle_J1_T1.mat',seed=7001,method='UAD',geometry_sample_time_s=float(z['t'][middle]),initial_radius_rad=rad,motion_radius_rad=float(rr)),indent=2)+'\n')
# Four-method descriptive confirmation, acceptance != outage.
colors=['#2166ac','#e08214','#4d9221','#984ea3'];fig,ax=plt.subplots(1,2,figsize=(10.4,3.4),constrained_layout=True);cases=['direction1_middle','direction2_middle'];x=np.arange(2)
for j,(method,label) in enumerate(names.items()):
 rr=[next(r for r in S if r['case_id']==c and r['method']==method) for c in cases];xx=x+(j-1.5)*.18
 if method!='lockin':ax[0].bar(xx,[100*int(r['accepted'])/600 for r in rr],width=.18,color=colors[j],label=label)
 ax[1].bar(xx,[float(r['mean_energy_urad2s']) for r in rr],width=.18,color=colors[j],label=label)
for aa in ax:aa.set_xticks(x,['R1 middle','R2 middle']);aa.grid(axis='y',alpha=.2);aa.set_axisbelow(True)
ax[0].set_ylabel('Accepted fits / 600 (%)');ax[0].set_ylim(0,108);ax[0].set_title('(a) Diagnostic acceptance');ax[0].legend(frameon=False,fontsize=10.5);ax[1].set_ylabel('Mean angular energy (µrad² s)');ax[1].set_title('(b) Excitation under equal time budget');ax[1].legend(frameon=False,fontsize=10.5)
fig.savefig(R/'matched_confirmation.pdf');plt.close(fig)
# Consistent paired sensitivity table rebuilt from preserved per-run rows.
old=load(ROOT/'research/v5/results/final/comparisons.csv');rob=[]
for condition in ['nominal','bias2','noise5']:
 rr=[r for r in old if r['condition']==condition and r['scenario']=='linear_drift' and r['method']=='UAD'];assert len(rr)==50
 acc=sum(float(r['accepted']) for r in rr);miss=sum(float(r['accepted']) and float(r['coverage_all_fits'])==0 for r in rr);bad=sum(float(r['accepted']) and float(r['accepted_error_um'])>1 for r in rr)
 rob.append(dict(condition=condition,n=50,accepted=int(acc),confidence_misses=int(miss),accepted_error_above_1um=int(bad)))
with (R/'sensitivity_summary.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=rob[0]);w.writeheader();w.writerows(rob)
fig,ax=plt.subplots(figsize=(3.45,2.3),constrained_layout=True);x=np.arange(3)
for j,(key,label,col) in enumerate([('accepted','Accepted','#2166ac'),('confidence_misses','Accepted outside radius','#b2182b'),('accepted_error_above_1um','Accepted error > 1 µrad','#e08214')]):ax.bar(x+(j-1)*.23,[r[key] for r in rob],.23,label=label,color=col)
ax.set_xticks(x,['Nominal','Bias','Noise ×5']);ax.set_ylim(0,78);ax.tick_params(labelsize=8);ax.set_ylabel('Trials out of 50',fontsize=8);ax.legend(fontsize=7,ncol=1,loc='upper center');fig.savefig(R/'premise_sensitivity.pdf');plt.close(fig)
print(rob)
