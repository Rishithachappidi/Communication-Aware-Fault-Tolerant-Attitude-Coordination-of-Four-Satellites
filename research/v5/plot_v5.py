"""Scientific figure from executed aggregate records; no illustrative invented data."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
here=Path(__file__).resolve().parent;out=here/'results/final';rows=list(csv.DictReader((out/'summary.csv').open()))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
methods=['DAP','UAD','guarded','lockin','lockin_native'];labels=['DAP','UAD','Fixed margin','ES 2.88 s','ES 8 s'];colors=['#737373','#225ea8','#41b6c4','#e6ab02','#a6761d']
fig,axes=plt.subplots(1,2,figsize=(10.5,3.6),constrained_layout=True)
for i,(metric,title) in enumerate([('mean_outage_s','(a) Affine drift: mean outage'),('mean_energy_urad2s','(b) Affine drift: angular excitation')]):
 vals=[float(next(r[metric] for r in rows if (r['condition'],r['scenario'],r['method'])==('nominal','linear_drift',m))) for m in methods]
 axes[i].bar(np.arange(5),vals,color=colors);axes[i].set_xticks(np.arange(5),labels,rotation=20,ha='right');axes[i].set_title(title);axes[i].set_ylabel('Seconds' if i==0 else r'$\mu$rad$^2$ s');axes[i].grid(axis='y',alpha=.2);axes[i].set_axisbelow(True)
 if i:axes[i].set_yscale('log')
fig.savefig(out/'budget_tradeoff.pdf');fig.savefig(out/'budget_tradeoff.png',dpi=200);plt.close(fig)
