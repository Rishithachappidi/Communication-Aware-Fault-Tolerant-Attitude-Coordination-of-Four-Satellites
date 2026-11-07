function report=test_v3
here=fileparts(mfilename('fullpath'));root=fileparts(fileparts(here));addpath(root);setup_project;addpath(here);
c=v3_config;[S,~]=dap_sequences;t=(0:7)';q=6e-6*S(:,:,1);b=[9;-4]*1e-6;
assert(norm([ones(1,8);t']*q,'fro')<1e-15);
P=eye(8)-[ones(8,1) t]*pinv([ones(8,1) t]);
assert(norm(q'*P*q-4*(6e-6)^2*eye(2),'fro')<1e-23);
% Invariance under arbitrary affine log-gain, including a large positive slope.
t=(0:31)'/10;q=repelem(q,4,1);c.targetRadius=5e-6;
for slope=[-0.6 0 0.4]
 gain=exp(-0.3+slope*(t-t(end)));
 power=c.p0*gain.*exp(-2*sum((q+b').^2,2)/c.alpha^2);
 f=dap_fit(t,q,power,c,1);assert(f.ok && norm(f.b-b)<1e-16);
end
% Rank failure and detector censoring must never yield a confident correction.
f=dap_fit(t,zeros(size(q)),power,c,1);assert(~f.ok && strcmp(f.reason,'rank'));
f=dap_fit(zeros(size(t)),q,power,c,1);assert(~f.ok && strcmp(f.reason,'temporal-rank'));
f=dap_fit(t,q,zeros(size(t)),c,1);assert(~f.ok && strcmp(f.reason,'censored'));
% Constant attenuation and offset are recovered together.
power=c.p0*0.6*exp(-2*sum((q+b').^2,2)/c.alpha^2);
f=dap_fit(t,q,power,c,0);assert(norm(f.b-b)<1e-16 && abs(f.gain-0.6)<1e-12);
% In the exact iid Gaussian log-noise model the stated ellipse is conservative.
rng(77);covered=0;for k=1:400
 f=dap_fit(t,q,power.*exp(c.sigma*randn(size(t))),c,1);
 covered=covered+(norm(f.b-b)<=f.radius);
end
assert(covered/400>=0.93);
c=v3_config;designs=v3_designs(c);p=dap_plan(0.41*c.p0,c,designs,true);
assert(~p.ok);p=dap_plan(0.18*c.p0,c,designs,true);assert(p.ok && p.riskSeconds<=c.acquisitionBudget);
% Half-step convergence of the imported continuous-time plant.
pa=terminal_parameters(c);u=[2e-6;-1e-6;1;1;1;0;zeros(4,1);1];
xa=zeros(8,1);xb=xa;for k=1:100
 xa=v3_advance(xa,u,zeros(5,1),pa,c.dt);
 xb=v3_advance(xb,u,zeros(5,1),pa,c.dt/2);xb=v3_advance(xb,u,zeros(5,1),pa,c.dt/2);
end
assert(norm(xa(1:2)-xb(1:2))<1e-9);
report=struct('checks',9,'status','passed','gaussian_coverage',covered/400,...
 'half_step_angle_difference_rad',norm(xa(1:2)-xb(1:2)),'matlab',version);
disp(report);
end
