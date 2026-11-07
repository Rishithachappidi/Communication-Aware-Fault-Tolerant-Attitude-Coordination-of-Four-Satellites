function x=v3_advance(x,u,z,p,dt)
% Fixed-step RK4 of the repository's original nonlinear terminal equations.
k1=terminal_kernel(x,u,z,p);k2=terminal_kernel(x+dt*k1/2,u,z,p);
k3=terminal_kernel(x+dt*k2/2,u,z,p);k4=terminal_kernel(x+dt*k3,u,z,p);
x=x+dt*(k1+2*k2+2*k3+k4)/6;
end
