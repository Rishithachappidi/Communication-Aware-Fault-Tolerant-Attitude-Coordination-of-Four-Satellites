function plan=uad_plan(pm,qm,c,lib,variant)
% Uncertainty-aware diagnosis (UAD): reference-relative, mission-envelope gate.
if nargin<5,variant='UAD';end
[lo,hi,mode]=power_envelope(pm,c);
plan=struct('ok',false,'q',zeros(8,2),'dwell',0.36,'amplitude',0,'riskSeconds',NaN,...
 'cost',Inf,'lower',[],'motion',[],'tube',[],'mode',mode,'powerLower',lo,'powerUpper',hi,...
 'reason','no-feasible-candidate','validTube',false);
if pm<=0.005*c.p0,plan.reason='detector-floor';return;end
if strcmp(variant,'point_gate')
 lo=pm;hi=pm;mode='service';if pm<c.sensitivity,mode='acquisition';end
 plan.mode=mode;
end
budget=c.serviceBudget;if strcmp(mode,'acquisition'),budget=c.acquisitionBudget;end
% The uncertain mode never unlocks the acquisition budget.
angleBound=sqrt(2)*c.kappa*c.noise;
Rprior=c.priorRadius+norm(qm)+angleBound;
Rpower=c.alphaRange(2)*sqrt(max(0,log(c.p0Range(2)*c.gainMax/max(lo,realmin)))/2);
R=min(Rprior,Rpower);
for k=1:numel(lib)
 d=lib(k);if ~d.valid || d.radius>c.targetRadius,continue;end
 displacement=d.motion-qm(:)';tube=d.tube+angleBound;
 if strcmp(variant,'no_tube'),tube=zeros(size(tube));end
 lower=relative_power_bound(lo,d.time,displacement,tube,[0;0],R,c.alphaRange(1),c.driftBound);
 risk=sum(lower<c.sensitivity)*c.dt;
 if risk>budget+1e-9,continue;end
 cost=d.duration+0.03*sum(d.motion(:).^2)*c.dt/1e-12;
 if cost<plan.cost
  plan.ok=true;plan.q=d.q;plan.dwell=d.dwell;plan.amplitude=d.amplitude;
  plan.riskSeconds=risk;plan.cost=cost;plan.lower=lower;plan.motion=d.motion;
  plan.tube=tube;plan.reason='selected';plan.validTube=d.valid;
 end
end
end
