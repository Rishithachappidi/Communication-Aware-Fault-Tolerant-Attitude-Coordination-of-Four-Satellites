function audit_measurement_units
[here,root]=v7_setup;config=v4_config;scales=[.25 .75 1];out=struct([]);maxError=0;
for scale=scales
 c=config;c.noise=config.noise*scale;c.powerNoise=config.powerNoise*scale;
 sigma_q=c.noise;sigma_v=2*c.noise;p=terminal_parameters(c);rng(8123);z=randn(700,5);x=zeros(8,1);u=[0;0;1;1;1;0;0;0;0;0;1];
 for i=1:700
  [~,y]=terminal_kernel(x,u,z(i,:)',p);
  expected=[x(1:2)+sigma_q*z(i,1:2)';x(3:4)+sigma_v*z(i,3:4)'];
  maxError=max(maxError,max(abs(y(19:22)-expected)));x=v4_advance(x,u,z(i,:)',p,c);
 end
 r=struct('noise_scale',scale,'sigma_q_rad',sigma_q,'sigma_v_rad_per_s',sigma_v,'coupling_gain_per_s',2,...
  'relative_power_sigma',c.powerNoise,'delta',c.delta,'N',ceil(c.T/c.dt),'channels',5,'kappa',c.kappa);
 if isempty(out),out=r;else,out(end+1)=r;end
end
assert(maxError<1e-18);report=struct('status','passed','kernel_sensor_samples',2100,'maximum_numerical_sensor_error',maxError,'rows',out,...
 'interpretation','Legacy coefficient2 is the declared numeric coupling gamma_v=2 s^-1 between distinct angle and rate noise scales; it is not a dimensionless equality of physical units. No inherited sensor values or old results changed.','calibration','Assumed source policy, not independently calibrated sensor hardware.');
fid=fopen(fullfile(here,'results','measurement_units.json'),'w');fprintf(fid,'%s',jsonencode(report,PrettyPrint=true));fclose(fid);disp(report);
end
