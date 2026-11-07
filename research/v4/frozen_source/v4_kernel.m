function [dx,y]=v4_kernel(x,u,z,p,c)
% Original controller/optics; true inertia and lag can differ from controller model.
[dx,y]=terminal_kernel(x,u,z,p);
J=c.J*c.actualJfactor;tau=c.tau*c.actualTaufactor;
dv=(x(5:6)-c.b*x(3:4))/J;
for a=1:2
 if abs(x(2+a))>=c.rateMax && sign(x(2+a))*dv(a)>0,dv(a)=0;end
end
dx(3:4)=dv;dx(5:6)=(u(3)*y(11:12)-x(5:6))/(tau*u(4));
end
