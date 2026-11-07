function f=dap_fit(t,q,p,c,degree)
% Drift-annihilating optical fit. Inputs are telemetry and nominal constants.
% q: N-by-2 measured angle in rad; p: N-by-1 measured received power in W.
% Reject censored windows rather than take logarithms of clipped darkness.
f=struct('ok',false,'b',[0;0],'gain',NaN,'radius',Inf,'residual',Inf,...
 'information',0,'covariance',nan(2),'reason','insufficient-data');
t=t(:);p=p(:);n=numel(t);
if n<12 || any(~isfinite([t;p;q(:)])),return;end
if any(p<=0.005*c.p0),f.reason='censored';return;end
tt=(t-t(end))/max(t(end)-t(1),eps); V=ones(n,degree+1);
for k=1:degree,V(:,k+1)=tt.^k;end
if rank(V)<degree+1,f.reason='temporal-rank';return;end
Q=q/c.alpha; z=log(p/c.p0)+2*sum(Q.^2,2);
[U,~]=qr(V,0); A=Q-U*(U'*Q); zz=z-U*(U'*z);
F=A'*A; f.information=min(eig(F));
if f.information<1e-5,f.reason='rank';return;end
h=F\(A'*zz); nuisance=V\(z-Q*h); residual=z-Q*h-V*nuisance;
f.b=-c.alpha*h/4; f.gain=exp(nuisance(1)+2*sum(f.b.^2)/c.alpha^2);
f.residual=sqrt(mean(residual.^2));
% Fixed nominal noise floor avoids a spuriously tiny confidence region.
sigma=max(c.sigma,sqrt(sum(residual.^2)/max(1,n-degree-3)));
f.covariance=c.alpha^2*sigma^2/16*(F\eye(2));
f.radius=sqrt(5.991464547*max(eig(f.covariance)));
f.ok=f.radius<=c.targetRadius && f.residual<=c.maxResidual && ...
 norm(f.b)<=c.priorRadius && f.gain>0.01 && f.gain<1.6;
if f.ok,f.reason='accepted';else,f.reason='model-or-confidence';end
end
