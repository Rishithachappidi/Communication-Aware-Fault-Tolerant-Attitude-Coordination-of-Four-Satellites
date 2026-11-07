function plan=guarded_plan(pm,qm,c,lib)
% Simpler fixed-margin robust heuristic: same optical envelope, no impulse tube.
% 2 urad fixed motion guard is declared before outcomes, not a guaranteed enclosure.
plan=struct('ok',false,'q',zeros(8,2),'dwell',0.36,'amplitude',0,'riskSeconds',NaN,...
 'cost',Inf,'lower',[],'motion',[],'tube',[],'mode','uncertain','powerLower',0,'powerUpper',Inf,...
 'reason','no-feasible-candidate','validTube',false);
[lo,hi,mode]=power_envelope(pm,c);plan.mode=mode;plan.powerLower=lo;plan.powerUpper=hi;
if pm<=0.005*c.p0,return;end
R=min(c.priorRadius+norm(qm)+sqrt(2)*c.kappa*c.noise,...
 c.alphaRange(2)*sqrt(max(0,log(c.p0Range(2)*c.gainMax/max(lo,realmin)))/2));
budget=c.serviceBudget;if strcmp(mode,'acquisition'),budget=c.acquisitionBudget;end
for k=1:numel(lib)
 a=lib(k);if ~a.valid||a.radius>c.targetRadius,continue;end
 rad=ones(size(a.time))*(2e-6+sqrt(2)*c.kappa*c.noise);
 d=a.motion-qm(:)';S=vecnorm(d,2,2)+rad;
 lower=lo*exp(-c.driftBound*a.time-2*(2*R*S+S.^2)/c.alphaRange(1)^2);
 risk=c.dt*sum(lower<c.sensitivity);cost=a.duration+.03*c.dt*sum(a.motion(:).^2)/1e-12;
 if risk<=budget+1e-9&&cost<plan.cost
  plan.ok=true;plan.q=a.q;plan.dwell=a.dwell;plan.amplitude=a.amplitude;
  plan.riskSeconds=risk;plan.cost=cost;plan.lower=lower;plan.motion=a.motion;
  plan.tube=rad;plan.reason='selected-fixed-margin-heuristic';
 end
end
end
