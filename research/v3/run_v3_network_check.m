function run_v3_network_check
here=fileparts(mfilename('fullpath'));name=build_v3_projection_model(4);
folder=fullfile(here,'results','network_integration');if ~isfolder(folder),mkdir(folder);end
rows=struct([]);
for scenario={'normal','pointing'}
 c=default_config(4);c.scenario=scenario{1};c.seed=101;c=prepare_config(c);
 base=run_case_v2(c,[],'v2');mw=get_param(name,'ModelWorkspace');assignin(mw,'cfg',c);
 tic;out=sim(name);runtime=toc;r=struct('config',c,'runtime',runtime,'t',out.plantLog.Time,'Y',timeseries_matrix(out.plantLog),...
  'D',timeseries_matrix(out.decisionLog),'E',timeseries_matrix(out.estimatorLog));
 assert(all(isfinite(r.Y),'all')&&all(isfinite(r.D),'all')&&all(isfinite(r.E),'all'));
 r.metrics=compute_metrics(r);save(fullfile(folder,[c.scenario '.mat']),'r','base');
 a=struct('scenario',c.scenario,'original_v2_metrics',base.metrics,'projection_adapter_metrics',r.metrics);
 if isempty(rows),rows=a;else,rows(end+1)=a;end
end
fid=fopen(fullfile(folder,'checks.json'),'w');fprintf(fid,'%s',jsonencode(rows,PrettyPrint=true));fclose(fid);
disp('Separate projection-only Simulink integration: two scenarios completed.');
close_system(name,0);close_system('SatelliteOpticalNetwork_4_v2',0);
end
