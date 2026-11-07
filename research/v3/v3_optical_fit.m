function [ok,offset,gain,condition,err]=v3_optical_fit(B,c)
% Adapter for the existing V2 history layout. Projection estimator only.
% The full service-aware planner is evaluated in v3_trial, not this adapter.
d=struct('p0',optical_power([0;0],1,false,c),'alpha',c.divergence,...
 'sigma',0.03,'targetRadius',2e-6,'maxResidual',0.08,'priorRadius',60e-6);
f=dap_fit(B(1,:)',B(2:3,:)',B(4,:)',d,1);
ok=f.ok;offset=f.b;gain=f.gain;condition=f.information;err=f.residual;
if ~isfinite(gain),gain=1;end
end
