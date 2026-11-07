function reproduce_v3
% Read-only use of V3 source, with all new outputs outside its directory.
here=fileparts(mfilename('fullpath'));root=fileparts(fileparts(here));
addpath(root);setup_project;addpath(fullfile(root,'research','v3'));
out=fullfile(here,'reproduction');if ~isfolder(out),mkdir(out);end
assert(~isfile(fullfile(out,'primary.csv')),'Audit reproduction already exists');
tests=test_v3;save(fullfile(out,'tests.mat'),'tests');
c=v3_config;designs=v3_designs(c);
names={'healthy','pointing','linear_drift','attenuation_only','quadratic_drift','fast_fading','deep_loss','near_threshold','dark'};
methods={'passive','constant_fit','projected_fixed','balanced_fixed','no_service','DAP'};
rows=struct([]);tic;
for name=names
 for seed=1001:1100
  for method=methods
   r=v3_trial(name{1},seed,method{1},c,designs);r=check_trace(r,c);r=rmfield(r,'trace');
   if isempty(rows),rows=r;else,rows(end+1)=r;end
  end
 end
 fprintf('Reproduced V3 %s: %.1fs\n',name{1},toc);
end
writetable(struct2table(rows),fullfile(out,'primary.csv'));
conditions={'fivefold_noise','actuator_mismatch','half_step'};rows=struct([]);
for condition=conditions
 c=v3_config;designs=v3_designs(c);
 switch condition{1}
  case 'fivefold_noise',c.noise=c.noise*5;c.powerNoise=c.powerNoise*5;
  case 'actuator_mismatch',c.J=c.J*1.25;c.tau=c.tau*1.5;
  case 'half_step',c.dt=c.dt/2;designs=v3_designs(c);
 end
 for name={'pointing','linear_drift','near_threshold','fast_fading'}
  for seed=2001:2100
   for method={'constant_fit','projected_fixed','DAP'}
    r=v3_trial(name{1},seed,method{1},c,designs);r=check_trace(r,c);r=rmfield(r,'trace');r.condition=condition{1};
    if isempty(rows),rows=r;else,rows(end+1)=r;end
   end
  end
 end
 fprintf('Reproduced V3 stress %s: %.1fs\n',condition{1},toc);
end
writetable(struct2table(rows),fullfile(out,'stress.csv'));
disp('V3 AUDIT REPRODUCTION COMPLETE: 9000 trials; per-trace outage/energy checks passed');
end
function r=check_trace(r,c)
z=r.trace;mask=z.t>=2;
assert(abs(sum(z.power(mask)<c.sensitivity)*c.dt-r.outage_s)<1e-10);
assert(abs(sum(sum(z.angle(z.probe,:).^2,2))*c.dt*1e12-r.energy_urad2s)<1e-8);
end
