function f=joint_ekf_fit(t,q,p,c)
% Independently implemented generic EKF baseline, not a reproduction of an optical paper.
% States [bx/alpha by/alpha log(g) dlog(g)/dt]. b is constant; drift is a random walk.
f=dap_fit(t,q,p,c,1);f.gainSE=Inf;
if numel(t)<12 || any(p<=0.005*c.p0),return;end
x=[0;0;0;0];P=diag([1 1 1 0.1]);
for k=1:numel(t)
 dt=0;if k>1,dt=t(k)-t(k-1);end
 A=eye(4);A(3,4)=dt;x=A*x;P=A*P*A'+diag([0 0 1e-5 1e-4])*dt;
 e=q(k,:)'/c.alpha+x(1:2);H=[-4*e' 1 0];
 pred=x(3)-2*sum(e.^2);var=c.powerNoise^2+16*(c.noise/c.alpha)^2*sum(e.^2);
 K=P*H'/(H*P*H'+max(var,1e-8));x=x+K*(log(p(k)/c.p0)-pred);
 P=(eye(4)-K*H)*P*(eye(4)-K*H)'+K*max(var,1e-8)*K';
end
f.b=x(1:2)*c.alpha;f.gain=exp(x(3));f.covariance=P(1:2,1:2)*c.alpha^2;
f.radius=sqrt(5.991464547*max(eig(f.covariance)));f.gainSE=sqrt(P(3,3));
f.ok=f.radius<=c.targetRadius && norm(f.b)<=c.priorRadius && f.gain>0.01 && f.gain<1.6;
f.reason='ekf-rejected';if f.ok,f.reason='accepted';end
end
