function run_v5
[here,root]=v5_setup;folder=fullfile(here,'results','final');assert(~isfolder(folder));mkdir(folder);
P=v5_protocol;fid=fopen(fullfile(folder,'protocol.json'),'w');fprintf(fid,'%s',jsonencode(P,PrettyPrint=true));fclose(fid);save(fullfile(folder,'protocol.mat'),'P');
% Freeze new and inherited decision implementation before new evaluation.
files=[dir(fullfile(here,'*.m'));dir(fullfile(root,'research','v4','*.m'));dir(fullfile(root,'research','v3','*.m'))];hashes=struct;
for i=1:numel(files)
 p=fullfile(files(i).folder,files(i).name);b=uint8(fileread(p));md=java.security.MessageDigest.getInstance('SHA-256');md.update(b);
 hashes.(matlab.lang.makeValidName(strrep(p,[root filesep],'')))=lower(reshape(dec2hex(typecast(md.digest(),'uint8'),2)',1,[]));
end
fid=fopen(fullfile(folder,'source_sha256.json'),'w');fprintf(fid,'%s',jsonencode(hashes,PrettyPrint=true));fclose(fid);
env=struct('matlab',version,'computer',computer,'created',char(datetime('now')));fid=fopen(fullfile(folder,'environment.json'),'w');fprintf(fid,'%s',jsonencode(env,PrettyPrint=true));fclose(fid);
rows=struct([]);tic;
for condition=P.conditions
 c=P.config;c.dwells=.36;c.noise=c.noise*condition.noise;c.powerNoise=c.powerNoise*condition.noise;c.sensorBias=[condition.bias;-.5*condition.bias]*1e-6;c.actualAlphaFactor=condition.beam;
 L=v4_library(c);legacy=v3_designs(c);
 for name=P.scenarios
  [rr,traces,passiveTraces]=trials(name{1},P.seeds,P.methods,c,L,legacy,condition.name,0,0);
  rows=append(rows,rr);save(fullfile(folder,sprintf('trial_%s_%s.mat',condition.name,name{1})),'traces','passiveTraces','c','-v7');
 end
 fprintf('New comparison %s: %d cumulative rows %.1fs\n',condition.name,numel(rows),toc);
end
writetable(struct2table(rows),fullfile(folder,'comparisons.csv'));rows=struct([]);
for jf=P.actuatorJ
 for tf=P.actuatorTau
  c=P.config;c.dwells=.36;c.actualJfactor=jf;c.actualTaufactor=tf;L=v4_library(c);legacy=v3_designs(c);
  for name=P.actuatorScenarios
   [rr,traces,passiveTraces]=trials(name{1},P.actuatorSeeds,P.actuatorMethods,c,L,legacy,'continuous_grid',jf,tf);
   rows=append(rows,rr);save(fullfile(folder,sprintf('grid_%g_%g_%s.mat',jf,tf,name{1})),'traces','passiveTraces','c','-v7');
  end
 end
 fprintf('Actuator grid J=%g: %d cumulative rows %.1fs\n',jf,numel(rows),toc);
end
writetable(struct2table(rows),fullfile(folder,'actuator_grid.csv'));disp('V5 COMPLETE');
end
function [rows,traces,passiveTraces]=trials(name,seeds,methods,c,L,legacy,condition,jf,tf)
rows=struct([]);traces=cell(numel(seeds),numel(methods));passiveTraces=cell(numel(seeds),1);
for a=1:numel(seeds)
 p=v5_trial(name,seeds(a),'passive',c,L,legacy);passiveTraces{a}=p.trace;
 for b=1:numel(methods)
  r=v5_trial(name,seeds(a),methods{b},c,L,legacy,p.trace);traces{a,b}=r.trace;r=rmfield(r,'trace');
  r.condition=condition;r.Jfactor=jf;r.taufactor=tf;
  rows=append(rows,r);
 end
end
end
function a=append(a,b)
if isempty(a),a=b;else,a=[a b];end
end
