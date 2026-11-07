function [Ad,Bd,A,B]=pid_discrete(c,Jfactor,taufactor)
% Exact algebra of the unsaturated RK4 discrete map, one axis, state [q v a I].
J=c.J*Jfactor;tau=c.tau*taufactor;d=c.b;
A=[0 1 0 0;0 -d/J 1/J 0;-c.J*c.kp/tau ...
 (c.b-c.J*c.kd)/tau -1/tau -c.J*c.ki/tau;1 0 0 0];
% inputs: reference angle, encoder noise, rate noise.
B=[0 0 0;0 0 0;c.J*c.kp/tau -c.J*c.kp/tau (c.b-c.J*c.kd)/tau;-1 1 0];
M=[A B;zeros(3,7)];Z=c.dt*M;E=eye(7)+Z+Z^2/2+Z^3/6+Z^4/24;
Ad=E(1:4,1:4);Bd=E(1:4,5:7);
end
