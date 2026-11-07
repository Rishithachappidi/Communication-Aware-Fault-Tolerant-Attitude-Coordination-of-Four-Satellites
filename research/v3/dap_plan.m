function plan=dap_plan(pNow,c,designs,enforceService)
% Finite-library optimization; no access to injected fault or future samples.
plan=struct('ok',false,'q',zeros(8,2),'dwell',0.35,'cost',Inf,...
 'riskSeconds',Inf,'radius',Inf,'amplitude',0,'reason','no-feasible-design');
if pNow<=0.005*c.p0,plan.reason='detector-floor';return;end
budget=c.serviceBudget;if pNow<c.sensitivity,budget=c.acquisitionBudget;end
for k=1:numel(designs)
 d=designs(k); if d.radius>c.targetRadius,continue;end
 % Bound the log-power change relative to the current position q=0.
 % Requires ||b||<=B and |d log g /dt|<=L over the entire probe horizon.
 lower=pNow*exp(-4*c.priorRadius*vecnorm(d.motion,2,2)/c.alpha^2 ...
   -2*sum(d.motion.^2,2)/c.alpha^2-c.driftBound*d.time);
 risk=sum(lower<c.sensitivity)*c.dt;
 if enforceService && risk>budget+1e-9,continue;end
 % Duration dominates; integrated angular energy breaks equal-time ties.
 cost=d.duration+0.03*sum(d.motion(:).^2)/1e-12*c.dt;
 if cost<plan.cost
  plan=struct('ok',true,'q',d.q,'dwell',d.dwell,'cost',cost,...
   'riskSeconds',risk,'radius',d.radius,'amplitude',d.amplitude,'reason','selected');
 end
end
end
