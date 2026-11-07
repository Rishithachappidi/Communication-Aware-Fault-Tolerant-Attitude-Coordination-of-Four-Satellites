"""Conditional probe authorization interface; no fault/recovery guarantee.
This module validates supplied evidence metadata and a bound budget. It cannot
verify the truth of a calibration report or guarantee a future fault stays fixed.
The caller/evidence authority is an explicit trust boundary.
"""
from dataclasses import dataclass,field
from math import isfinite,ceil
from statistics import NormalDist
FINITE_MODELS={(j,t) for j in (.8,1.,1.25) for t in (1.,1.5)}
REQUIRED=('sensor_calibration','actuator_identification','optical_bounds','constant_offset_window','gain_slope_window','zero_reference_history','bound_implementation')
@dataclass
class Evidence:
    actuator_pair:tuple[float,float]
    references:dict[str,str]=field(default_factory=dict)
    valid_until:float=0.
    provenance:str='simulation'
    angular_unit:str='rad'
    power_unit:str='W'
    tail_model:str='Gaussian with stipulated marginal scales'
    channels:int=5
    horizon_samples:int=700
    delta:float=.01
    relative_power_sigma:float=.008

def authorize(lower,dt,duration,pm,threshold,evidence,now=0.,deployment='simulation',service_budget=0.,acquisition_budget=4.):
    reasons=[]
    if not isinstance(evidence,Evidence):return {'permission':'refuse','reasons':['evidence unavailable'],'recovery_authorized':False}
    for name in REQUIRED:
        if not isinstance(evidence.references.get(name),str) or not evidence.references[name].strip():reasons.append('missing '+name)
    if evidence.actuator_pair not in FINITE_MODELS:reasons.append('actual model not in finite set')
    if not isfinite(now) or not isfinite(evidence.valid_until) or evidence.valid_until<now+duration:reasons.append('evidence does not cover probe window')
    if (evidence.angular_unit,evidence.power_unit)!=('rad','W'):reasons.append('unit mismatch')
    if deployment!='simulation' and evidence.provenance!='external-verified':reasons.append('simulation evidence cannot authorize deployment')
    if evidence.tail_model!='Gaussian with stipulated marginal scales' or evidence.channels!=5:reasons.append('uncalibrated tail/channel model')
    if not (isfinite(dt) and dt>0 and isfinite(duration) and duration>0):reasons.append('invalid timing')
    if not (isfinite(pm) and pm>=0 and isfinite(threshold) and threshold>0):reasons.append('invalid power')
    if not (0<evidence.delta<1 and isinstance(evidence.horizon_samples,int) and evidence.horizon_samples>=1):reasons.append('invalid mission envelope')
    if not all(isfinite(v) and v>=0 for v in (service_budget,acquisition_budget)):reasons.append('invalid outage budget')
    if isinstance(lower,(list,tuple)) and len(lower)>evidence.horizon_samples:reasons.append('envelope horizon shorter than probe')
    if reasons:return {'permission':'refuse','reasons':reasons,'recovery_authorized':False}
    k=NormalDist().inv_cdf(1-evidence.delta/(2*evidence.channels*evidence.horizon_samples));eta=k*evidence.relative_power_sigma
    if not isfinite(eta) or eta<0 or eta>=1:return {'permission':'refuse','reasons':['uninformative multiplicative envelope'],'recovery_authorized':False}
    if len(lower)!=ceil(duration/dt-1e-8) or not all(isfinite(x) and x>=0 for x in lower):return {'permission':'refuse','reasons':['invalid lower-bound record'],'recovery_authorized':False}
    upper=pm/(1-eta);mode='acquisition' if upper<threshold else 'service-or-uncertain'
    budget=acquisition_budget if mode=='acquisition' else service_budget;risk=sum(x<threshold for x in lower)*dt
    if risk>budget+1e-9:return {'permission':'refuse','mode':mode,'reasons':['sampled budget exceeded'],'recovery_authorized':False}
    return {'permission':'conditional-probe','mode':mode,'measurement_eta':eta,'predicted_sampled_outage_s':risk,'budget_s':budget,'assumption_references':dict(evidence.references),'recovery_authorized':False,'scope':'Conditional on supplied evidence being correct and remaining valid; sampled probe window only.'}

def monitor(sample_power,predicted_lower,eta=0.):
    if not isfinite(eta) or eta<0 or eta>=1:return {'event':'invalid-sensor','request':'inhibit probe, envelope unavailable'}
    if not isfinite(sample_power) or sample_power<0:return {'event':'invalid-sensor','request':'inhibit probe, follow validated fallback policy'}
    if sample_power/(1-eta)+1e-14<predicted_lower:return {'event':'bound-breach','request':'mark uncertified, inhibit repeated probing, request validated neutral-controller fallback'}
    return {'event':'no-observed-breach','request':'continue subject to the declared contract'}
