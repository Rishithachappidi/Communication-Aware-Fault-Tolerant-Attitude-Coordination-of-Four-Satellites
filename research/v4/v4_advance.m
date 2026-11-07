function x=v4_advance(x,u,z,p,c)
h=c.dt;k1=v4_kernel(x,u,z,p,c);k2=v4_kernel(x+h*k1/2,u,z,p,c);
k3=v4_kernel(x+h*k2/2,u,z,p,c);k4=v4_kernel(x+h*k3,u,z,p,c);
x=x+h*(k1+2*k2+2*k3+k4)/6;
end
