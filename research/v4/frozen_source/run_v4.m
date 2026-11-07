function folder=run_v4(tag)
if nargin<1,tag='final';end
[here,root]=v4_setup;folder=fullfile(here,'results',tag);
assert(~isfolder(folder),'Refusing to overwrite existing experiment folder');mkdir(folder);
P=v4_protocol;testReport=test_v4;
% Freeze configuration and source BEFORE seeing final evaluation outcomes.
fid=fopen(fullfile(folder,'protocol.json'),'w');fprintf(fid,'%s',jsonencode(P,PrettyPrint=true));fclose(fid);
save(fullfile(folder,'protocol.mat'),'P','testReport');
files=dir(fullfile(here,'*.m'));hashes=struct;
for k=1:numel(files)
 bytes=uint8(fileread(fullfile(files(k).folder,files(k).name)));
 digest=java.security.MessageDigest.getInstance('SHA-256');digest.update(bytes);
 hash=lower(reshape(dec2hex(typecast(digest.digest(),'uint8'),2)',1,[]));
 hashes.(matlab.lang.makeValidName(files(k).name))=hash;
end
fid=fopen(fullfile(folder,'source_sha256.json'),'w');fprintf(fid,'%s',jsonencode(hashes,PrettyPrint=true));fclose(fid);
environment=struct('matlab',version,'computer',computer,'created',char(datetime('now')),...
 'root',root,'testReport',testReport,'pidPredictor','finite-model unsaturated RK4, verified stage constraints');
fid=fopen(fullfile(folder,'environment.json'),'w');fprintf(fid,'%s',jsonencode(environment,PrettyPrint=true));fclose(fid);
rows=struct([]);c=P.config;L=v4_library(c);legacy=v3_designs(c);tic;
for name=P.scenarios
 [new,traces]=condition_trials(name{1},P.primarySeeds,P.methods,c,L,legacy,'primary',0);
 rows=append(rows,new);save(fullfile(folder,['primary_' name{1} '.mat']),'traces','c','-v7.3');
 fprintf('PRIMARY %s: %d trials, %.1f s\n',name{1},numel(new),toc);
end
writetable(struct2table(rows),fullfile(folder,'primary.csv'));
rows=struct([]);
for sweep=P.sweeps
 for value=sweep.values
  c=sweep_config(P.config,sweep.name,value);L=v4_library(c);legacy=v3_designs(c);
  for name=sweep.scenarios
   [new,traces]=condition_trials(name{1},P.sensitivitySeeds,sweep.methods,c,L,legacy,sweep.name,value);
   rows=append(rows,new);
   file=sprintf('sensitivity_%s_%g_%s.mat',sweep.name,value,name{1});
   save(fullfile(folder,file),'traces','c','-v7.3');
  end
  fprintf('SENSITIVITY %s %g: %d cumulative trials, %.1f s\n',sweep.name,value,numel(rows),toc);
 end
 writetable(struct2table(rows),fullfile(folder,'sensitivity_checkpoint.csv'));
end
writetable(struct2table(rows),fullfile(folder,'sensitivity.csv'));
disp('V4 FINAL EXECUTION COMPLETE');
end
function [rows,traces]=condition_trials(name,seeds,methods,c,L,legacy,condition,value)
rows=struct([]);traces=cell(numel(seeds),numel(methods));
for a=1:numel(seeds)
 passive=v4_trial(name,seeds(a),'passive',c,L,legacy);counterfactual=passive.trace;
 for j=1:numel(methods)
  if strcmp(methods{j},'passive'),r=passive;r.probe_induced_outage_s=0;r.avoided_outage_s=0;
  else,r=v4_trial(name,seeds(a),methods{j},c,L,legacy,counterfactual);end
  traces{a,j}=r.trace;r=rmfield(r,'trace');r.condition=condition;r.condition_value=value;
  if isempty(rows),rows=r;else,rows(end+1)=r;end
 end
end
end
function a=append(a,b)
if isempty(a),a=b;else,a=[a b];end
end
