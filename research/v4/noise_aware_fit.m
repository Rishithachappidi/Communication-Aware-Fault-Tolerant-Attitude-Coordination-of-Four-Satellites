function f=noise_aware_fit(t,q,p,c,degree)
% Iterated feasible GLS with first-order angle-error variance. Not exact EIV MLE.
f=dap_fit(t,q,p,c,degree);f.gainSE=Inf;f.whitenedStatistic=Inf;
if numel(t)<12 || any(p<=0.005*c.p0) || f.information<1e-5,return;end
n=numel(t);s=(t(:)-t(end))/max(t(end)-t(1),eps);V=ones(n,degree+1);
for j=1:degree,V(:,j+1)=s.^j;end
Q=q/c.alpha;X=[V Q];
% Second-order mean correction for independent zero-mean encoder/power noise.
z=log(p(:)/c.p0)+2*sum(Q.^2,2)+c.powerNoise^2/2-4*c.noise^2/c.alpha^2;
beta=X\z;b=-c.alpha*beta(end-1:end)/4;
for it=1:c.maxFitIterations
 variance=max(1e-8,c.powerNoise^2+16*c.noise^2*sum((q+b').^2,2)/c.alpha^4);
 W=1./sqrt(variance);A=X.*W;bb=A\(z.*W);
 if norm(bb-beta)<1e-7,beta=bb;break;end
 beta=bb;b=-c.alpha*beta(end-1:end)/4;
end
b=-c.alpha*beta(end-1:end)/4;res=z-X*beta;stat=sum(res.^2./variance);
covbeta=(A'*A)\eye(size(A,2));covb=c.alpha^2/16*covbeta(end-1:end,end-1:end);
f.b=b;f.covariance=covb;f.radius=sqrt(5.991464547*max(eig(covb)));
f.gain=exp(beta(1)+2*sum(b.^2)/c.alpha^2);
jac=zeros(size(beta));jac(1)=1;jac(end-1:end)=-b/c.alpha;
f.gainSE=sqrt(max(0,jac'*covbeta*jac));f.residual=sqrt(mean(res.^2));
dof=n-size(X,2);upper=2*gammaincinv(1-c.fitAlpha,dof/2);
f.whitenedStatistic=stat;f.ok=stat<=upper && f.radius<=c.targetRadius && ...
 norm(b)<=c.priorRadius && f.gain>0.01 && f.gain<1.6;
f.reason='noise-aware-rejected';if f.ok,f.reason='accepted';end
end
