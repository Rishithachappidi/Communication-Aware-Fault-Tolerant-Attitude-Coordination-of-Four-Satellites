function f=parameter_kf_fit(t,q,p,c)
% Generic linear Kalman parameter filter on the exact log-Gaussian transform.
% State [h_x,h_y,nuisance_intercept_at_current_time,log_gain_slope].
f=dap_fit(t,q,p,c,1);f.gainSE=Inf;
if numel(t)<12 || any(p<=0.005*c.p0),return;end
x=zeros(4,1);P=diag([36 36 4 0.1]);Qvar=c.kfProcess;
for k=1:numel(t)
 dt=0;if k>1,dt=t(k)-t(k-1);end
 A=eye(4);A(3,4)=dt;x=A*x;P=A*P*A'+diag([0 0 Qvar Qvar/10])*dt;
 b=-c.alpha*x(1:2)/4;H=[q(k,:)/c.alpha 1 0];
 obs=log(p(k)/c.p0)+2*sum(q(k,:).^2)/c.alpha^2+c.powerNoise^2/2-4*c.noise^2/c.alpha^2;
 variance=max(1e-8,c.powerNoise^2+16*c.noise^2*sum((q(k,:)'+b).^2)/c.alpha^4);
 K=P*H'/(H*P*H'+variance);x=x+K*(obs-H*x);
 P=(eye(4)-K*H)*P*(eye(4)-K*H)'+K*variance*K';
end
f.b=-c.alpha*x(1:2)/4;f.gain=exp(x(3)+2*sum(f.b.^2)/c.alpha^2);
f.covariance=c.alpha^2/16*P(1:2,1:2);f.radius=sqrt(5.991464547*max(eig(f.covariance)));
jac=[-f.b/c.alpha;1;0];f.gainSE=sqrt(max(0,jac'*P*jac));
f.ok=f.radius<=c.targetRadius&&norm(f.b)<=c.priorRadius&&f.gain>0.01&&f.gain<1.6;
f.reason='kf-rejected';if f.ok,f.reason='accepted';end
end
