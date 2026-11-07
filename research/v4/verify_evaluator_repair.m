function verify_evaluator_repair
[here,~]=v4_setup;folder=fullfile(here,'results','final');T=readtable(fullfile(folder,'sensitivity_corrected.csv'));
X=T(T.certificate_premises_recorded==1&T.certificate_premises==0,:);
c=sweep_config(v4_config,'beam',0.9);L=v4_library(c);legacy=v3_designs(c);
ignore={'plan_runtime_s','fit_runtime_s','condition','condition_value','certificate_premises_recorded'};
for i=1:height(X)
 passive=v4_trial(X.scenario{i},X.seed(i),'passive',c,L,legacy);
 r=v4_trial(X.scenario{i},X.seed(i),X.method{i},c,L,legacy,passive.trace);r=rmfield(r,'trace');
 names=fieldnames(r);
 for j=1:numel(names)
  key=names{j};if ismember(key,ignore),continue;end
  expected=X.(key)(i,:);value=r.(key);
  if isnumeric(value)||islogical(value)
   assert((isnan(value)&&isnan(expected))||value==expected||abs(value-expected)<1e-9,key);
  else,assert(strcmp(value,expected{1}),key);end
 end
end
report=struct('status','passed','reexecuted_cases',height(X),...
 'result','All non-timing metrics match the explicitly corrected records; only the premise logging changed.');
fid=fopen(fullfile(folder,'evaluator_repair_replay.json'),'w');fprintf(fid,'%s',jsonencode(report,PrettyPrint=true));fclose(fid);disp(report);
end
