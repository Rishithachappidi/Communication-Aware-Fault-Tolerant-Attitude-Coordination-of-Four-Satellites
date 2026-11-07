function audit_saved_binary
here=fileparts(mfilename('fullpath'));root=fileparts(fileparts(here));addpath(root);setup_project;addpath(fullfile(root,'research','v3'));
v3=fullfile(root,'research','v3');A=load(fullfile(v3,'results','full','all_results.mat'));
compare(A.T,readtable(fullfile(v3,'results','full','trials.csv')));
names=fieldnames(A.examples);traceCount=0;
for i=1:numel(names)
 methods=fieldnames(A.examples.(names{i}));
 for j=1:numel(methods)
  z=A.examples.(names{i}).(methods{j});row=A.T(strcmp(A.T.scenario,names{i})&strcmp(A.T.method,methods{j})&A.T.seed==1001,:);
  dt=A.protocol.config.dt;assert(abs(sum(~z.available(z.t>=2))*dt-row.outage_s)<1e-10);
  traceCount=traceCount+1;
 end
end
B=load(fullfile(v3,'results','stress','records.mat'));compare(B.T,readtable(fullfile(v3,'results','stress','trials.csv')));
for name={'normal','pointing'}
 X=load(fullfile(v3,'results','network_integration',[name{1} '.mat']));
 for var={'r','base'}
  y=X.(var{1});m=compute_metrics(y);assert(isequaln(m,y.metrics));
 end
end
report=struct('status','passed','primary_binary_rows',height(A.T),'sensitivity_binary_rows',height(B.T),...
 'representative_trace_checks',traceCount,'saved_simulink_metric_reconstructions',4);
fid=fopen(fullfile(here,'SAVED_BINARY_AUDIT.json'),'w');fprintf(fid,'%s',jsonencode(report,PrettyPrint=true));fclose(fid);disp(report);
end
function compare(a,b)
assert(height(a)==height(b)&&isequal(a.Properties.VariableNames,b.Properties.VariableNames));
for k=1:width(a)
 aa=a{:,k};bb=b{:,k};
 if isnumeric(aa)||islogical(aa),assert(all(aa==bb | abs(double(aa)-double(bb))<1e-10 | (isnan(aa)&isnan(bb))));
 else,assert(isequal(string(aa),string(bb)));end
end
end
