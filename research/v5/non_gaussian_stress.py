"""Out-of-model tail calibration stress, not a plant experiment or theorem."""
from independent_checks import *
from scipy.stats import t as student_t
rng=np.random.default_rng(17026);N=700;k=ndtri(1-.01/(10*N));missions=1000;fail=0;false=0
for i in range(10):
 Z=rng.standard_t(5,(100,N,5))/math.sqrt(5/3)
 inside=np.max(np.abs(Z),axis=(1,2))<=k;fail+=int((~inside).sum())
 pm=np.maximum(0,1.00001*(1+.08*Z[:,:,4]));upper=pm.min(axis=1)/(1-k*.08)
 false+=int((upper<1).sum());assert not np.any((upper<1)&inside)
tail=float(2*student_t.sf(k*math.sqrt(5/3),5));out={'status':'executed_out_of_model','distribution':'Student-t5, independently sampled and rescaled to unit variance','missions':missions,'global_event_failures':fail,'selected_minimum_false_acquisitions':false,'single_marginal_tail':tail,'independent_global_event_failure_theory':1-(1-tail)**(5*N),'scope':'Same variance does not justify Gaussian kappa. This synthetic adverse-time test is not the optical plant trigger; it invalidates transferring Gaussian calibration to these tails.'}
dump('non_gaussian.json',out);print(out)
