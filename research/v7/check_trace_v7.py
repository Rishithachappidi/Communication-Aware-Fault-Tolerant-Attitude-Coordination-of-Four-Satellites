"""Preserved independent trace checker with explicit finite-horizon fit completion.
Only fit_rejected predicate extends V5: an unfinished probe has no fit to reject.
All other numerical checks retained. Historical source/exports untouched.
"""
import numpy as np
import math,h5py
from independent_checks import truth,read,scalar
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
 same('false_correction',int(np.linalg.norm(b[-1])==0 and np.linalg.norm(val('correction'))>c['offsetThreshold']));same('missed_pointing_diagnosis',int(np.linalg.norm(b[-1])>c['offsetThreshold'] and not float(row['accepted'])));same('missed_diagnosis',int((np.linalg.norm(b[-1])>0 or abs(g[-1]-1)>1e-10) and not float(row['accepted'])));same('abstained',int(bool(float(row['attempted'])) and not probe.any()));same('fit_rejected',int(bool(probe.any()) and np.isfinite(float(row['finish_s'])) and not float(row['accepted']) and row['method'] not in ['lockin','lockin_native']));same('tail_availability',np.mean(~down[t>=12]));same('probe_induced_outage_s',np.sum(down[mask]&~passive[mask])*dt);same('avoided_outage_s',np.sum(~down[mask]&passive[mask])*dt)
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
