function report=test_v4
v4_setup;c=v4_config;checks={};rng(901);
% 1. Sharp ball/ball angular loss: random containment and attained equality.
for k=1:2000
 d=randn(1,2)*5e-6;R=rand*30e-6;r=rand*2e-6;
 [~,D]=relative_power_bound(1,0,d,r,[0;0],R,c.alpha,0);
 v=d/norm(d);e=R*v;actuald=d+r*v;
 assert(abs(D-(2*e*actuald'+sum(actuald.^2)))<1e-22);
 e=R*rand*unit(randn(1,2));dd=d+r*rand*unit(randn(1,2));
 assert(2*e*dd'+sum(dd.^2)<=D+1e-22);
end
checks{end+1}='sharp angular loss and containment';
% 2. Relative measurement envelope including adaptively selectable endpoints.
for z=linspace(-c.kappa,c.kappa,101)
 truth=1.02*c.sensitivity;[lo,hi,mode]=power_envelope(truth*(1+c.powerNoise*z),c);
 assert(lo<=truth+1e-20 && hi>=truth-1e-20 && ~strcmp(mode,'acquisition'));
end
checks{end+1}='simultaneous-envelope acquisition gate';
% 3. Discrete PID predictor exactly matches the unsaturated imported RK4 equations.
for jf=c.Jfactors
 for tf=c.taufactors
  cc=c;cc.actualJfactor=jf;cc.actualTaufactor=tf;
  [Ad,Bd]=pid_discrete(cc,jf,tf);x=randn(8,1).*[ones(4,1)*1e-7;ones(2,1)*1e-9;ones(2,1)*1e-8];
  z=randn(5,1);ref=[2;-1]*1e-6;u=[ref;1;1;1;0;zeros(4,1);1];
  xx=v4_advance(x,u,z,terminal_parameters(c),cc);
  for a=1:2
   ix=[a a+2 a+4 a+6];pred=Ad*x(ix)+Bd*[ref(a);c.noise*z(a);2*c.noise*z(a+2)];
   assert(norm(pred-xx(ix))<1e-15);
  end
 end
end
checks{end+1}='finite-model RK4 predictor exactness';
% 4. Noiseless offset/gain identification, affine invariance and temporal rank.
[S,~]=dap_sequences;q=repelem(S(:,:,1),6,1)*6e-6;t=(0:size(q,1)-1)'/20;b=[10;-5]*1e-6;
cc=c;cc.noise=0;cc.powerNoise=0;cc.sigma=1e-8;
p=cc.p0*exp(-0.2-0.09*(t-t(end))).*exp(-2*sum((q+b').^2,2)/cc.alpha^2);
f=noise_aware_fit(t,q,p,cc,1);assert(f.ok&&norm(f.b-b)<1e-12&&abs(f.gain-exp(-0.2))<1e-8);
f=noise_aware_fit(t,zeros(size(q)),p,cc,1);assert(~f.ok);
checks{end+1}='noiseless affine identification and rank rejection';
% 5. Covariance unit/scale verification against independent direct linear algebra.
Q=q/c.alpha;V=[ones(size(t)) t];PV=eye(numel(t))-V*pinv(V);F=Q'*PV*Q;
cc=c;cc.targetRadius=10e-6;pp=c.p0*exp(-2*sum((q+b').^2,2)/c.alpha^2);
expected=c.alpha^2*c.sigma^2/16*inv(F);f=dap_fit(t,q,pp,cc,1);
assert(norm(f.covariance-expected,'fro')<1e-24);
checks{end+1}='covariance transformation and units';
% 6. Unmodeled component in span(Q) has zero residual but a biased offset.
dd=[0.1;-0.05];pm=pp.*exp(Q*dd);f=dap_fit(t,q,pm,cc,1);
assert(f.residual<1e-10 && norm(f.b-b)>1e-7);
checks{end+1}='unobservable model-mismatch counterexample';
% 7. Candidate score and feasible selection, darkness and uncertain-service refusal.
lib=v4_library(c);plan=uad_plan(0.18*c.p0,[0;0],c,lib);
assert(plan.ok&&plan.riskSeconds<=c.acquisitionBudget);
costs=[];for d=lib
 if d.valid && d.radius<=c.targetRadius && d.duration<=c.acquisitionBudget+1e-9
  costs(end+1)=d.duration+0.03*sum(d.motion(:).^2)*c.dt/1e-12;
 end
end
assert(abs(plan.cost-min(costs))<1e-10);
assert(~uad_plan(0,[0;0],c,lib).ok);
assert(~uad_plan(0.41*c.p0,[0;0],c,lib).ok);
checks{end+1}='candidate selection and infeasible abstention';
% 8. Closed-loop healthy/deep-loss behavior and same-seed determinism.
legacy=v3_designs(c);a=v4_trial('healthy',31,'UAD',c,lib,legacy);
assert(~a.attempted&&a.probe_count==0&&a.outage_s==0);
a=v4_trial('deep_loss',31,'UAD',c,lib,legacy);assert(norm(a.trace.correction)==0);
a=v4_trial('linear_drift',31,'UAD',c,lib,legacy);bb=v4_trial('linear_drift',31,'UAD',c,lib,legacy);
assert(isequaln(a.trace,bb.trace)&&~a.bound_violation&&~a.tube_violation);
checks{end+1}='closed-loop requirements and determinism';
% 9. Integral aperture check, independently evaluated without the small-aperture approximation.
alpha=c.alpha;w=c.distance*alpha;ra=c.aperture/2;relative=[];
for theta=linspace(0,60e-6,20)
 distance=c.distance*theta;
 exact=c.Pt*c.eta*4/w^2*exp(-2*distance^2/w^2)*integral(@(r)r.*exp(-2*r.^2/w^2).*besseli(0,4*r*distance/w^2),0,ra,'AbsTol',1e-18);
 approx=optical_power([theta;0],1,false,c);relative(end+1)=abs(approx-exact)/exact;
end
assert(max(relative)<0.001);checks{end+1}='independent finite-aperture quadrature';
% 10. Abrupt offset onset during an early probe invalidates the static-offset premise.
cc=c;cc.actualAlphaFactor=0.9;
r=v4_trial('pointing',4001,'UAD',cc,lib,legacy);
assert(r.start_s<2&&r.finish_s>2&&r.bound_violation&&~r.certificate_premises);
checks{end+1}='mid-probe fault premise regression';
report=struct('status','passed','count',numel(checks),'checks',{checks},...
 'aperture_max_relative_error',max(relative),'matlab',version);
disp(report);
end
function y=unit(x)
y=x/norm(x);
end
