function designs=v3_designs(c)
% Predict each candidate with the same nominal actuator dynamics as the plant.
[S,~]=dap_sequences;designs=struct([]);p=terminal_parameters(c);
for dwell=[0.35 0.5]
 for amp=[1 2 4 6]*1e-6
  q=amp*S(:,:,1);t=(0:c.dt:8*dwell-c.dt)';x=zeros(8,1);motion=zeros(numel(t),2);
  for k=1:numel(t)
   phase=min(8,floor((t(k)+1e-9)/dwell)+1);
   u=[q(phase,:)';1;1;1;0;zeros(4,1);1];
   [~,y]=terminal_kernel(x,u,zeros(5,1),p);motion(k,:)=y(3:4)';
   x=v3_advance(x,u,zeros(5,1),p,c.dt);
  end
  keep=mod(t+1e-9,dwell)>=c.settleFraction*dwell;
  ideal=c.p0*exp(-2*sum(motion.^2,2)/c.alpha^2);
  f=dap_fit(t(keep),motion(keep,:),ideal(keep),c,1);
  d=struct('q',q,'time',t,'motion',motion,'dwell',dwell,'duration',8*dwell,...
    'radius',f.radius,'amplitude',amp);
  if isempty(designs),designs=d;else,designs(end+1)=d;end
 end
end
end
