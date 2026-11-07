function run_v3_stress(tag)
% Additional sensitivity experiments. Primary protocol/results stay unchanged.
here=fileparts(mfilename('fullpath'));root=fileparts(fileparts(here));addpath(root);setup_project;addpath(here);
if nargin<1,tag='stress';end
folder=fullfile(here,'results',tag);if ~isfolder(folder),mkdir(folder);end
assert(~isfile(fullfile(folder,'trials.csv')),'Completed stress results already exist');
names={'pointing','linear_drift','near_threshold','fast_fading'};
methods={'constant_fit','projected_fixed','DAP'};
conditions={'fivefold_noise','actuator_mismatch','half_step'};
rows=struct([]);base=v3_config;nominalDesigns=v3_designs(base);tic;
for a=1:numel(conditions)
 c=base;designs=nominalDesigns;
 switch conditions{a}
  case 'fivefold_noise',c.noise=5*c.noise;c.powerNoise=5*c.powerNoise;
  case 'actuator_mismatch',c.J=1.25*c.J;c.tau=1.5*c.tau;
  case 'half_step',c.dt=c.dt/2;designs=v3_designs(c);
 end
 for name=names
  for seed=2001:2100
   for method=methods
    r=v3_trial(name{1},seed,method{1},c,designs);r=rmfield(r,'trace');
    r.condition=conditions{a};if isempty(rows),rows=r;else,rows(end+1)=r;end
   end
  end
 end
 fprintf('%s completed after %.1f s\n',conditions{a},toc);
end
T=struct2table(rows);writetable(T,fullfile(folder,'trials.csv'));
save(fullfile(folder,'records.mat'),'T','base','nominalDesigns');
summary=struct([]);
for a=1:numel(conditions)
 for name=names
  for method=methods
   X=T(strcmp(T.condition,conditions{a})&strcmp(T.scenario,name{1})&strcmp(T.method,method{1}),:);
   r=struct('condition',conditions{a},'scenario',name{1},'method',method{1},'n',height(X),...
    'accepted',sum(X.accepted),'rejected',sum(X.rejected),...
    'median_error_um',median(X.error_um,'omitnan'),'mean_outage_s',mean(X.outage_s),...
    'conditional_coverage',mean(X.coverage,'omitnan'));
   if isempty(summary),summary=r;else,summary(end+1)=r;end
  end
 end
end
writetable(struct2table(summary),fullfile(folder,'summary.csv'));
fprintf('STRESS COMPLETE: %d trials\n',height(T));
end
