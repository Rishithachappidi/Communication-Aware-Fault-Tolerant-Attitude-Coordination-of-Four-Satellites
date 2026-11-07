function folder=run_v3(mode)
if nargin<1,mode='full';end
here=fileparts(mfilename('fullpath'));root=fileparts(fileparts(here));addpath(root);setup_project;addpath(here,fullfile(root,'revisions','v2'));
folder=fullfile(here,'results',mode);if ~isfolder(folder),mkdir(folder);end
assert(~isfile(fullfile(folder,'trials.csv')),'Existing completed results: use another mode/output directory.');
testReport=test_v3;c=v3_config;designs=v3_designs(c);
names={'healthy','pointing','linear_drift','attenuation_only','quadratic_drift',...
 'fast_fading','deep_loss','near_threshold','dark'};
methods={'passive','constant_fit','projected_fixed','balanced_fixed','no_service','DAP'};
seeds=1001:1100;if strcmp(mode,'smoke'),seeds=17:18;end
protocol=struct('config',c,'scenarios',{names},'methods',{methods},'seeds',seeds,...
 'comparison','paired common random numbers; same trigger; one diagnosis attempt',...
 'plant','original terminal_kernel, PID controller, fixed-step RK4',...
 'designs',designs,'testReport',testReport,'matlab',version);
save(fullfile(folder,'protocol.mat'),'protocol');
fid=fopen(fullfile(folder,'protocol.json'),'w');fprintf(fid,'%s',jsonencode(protocol,PrettyPrint=true));fclose(fid);
rows=struct([]);examples=struct;tic;
for a=1:numel(names)
 for seed=seeds
  for j=1:numel(methods)
   r=v3_trial(names{a},seed,methods{j},c,designs);
   if seed==seeds(1),examples.(names{a}).(methods{j})=r.trace;end
   r=rmfield(r,'trace');if isempty(rows),rows=r;else,rows(end+1)=r;end
  end
 end
 fprintf('%s: %d paired seeds completed (%.1f s)\n',names{a},numel(seeds),toc);
 save(fullfile(folder,'checkpoint.mat'),'rows','examples','protocol');
end
elapsed=toc;T=struct2table(rows);writetable(T,fullfile(folder,'trials.csv'));
save(fullfile(folder,'all_results.mat'),'T','examples','protocol','elapsed','-v7.3');
v3_summarize(folder,T,examples,protocol);fprintf('COMPLETE: %d trials, %.2f seconds\n',height(T),elapsed);
end
