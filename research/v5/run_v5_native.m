function run_v5_native
[here,~]=v5_setup;folder=fullfile(here,'results','native');assert(~isfolder(folder));mkdir(folder);P=v5_protocol;
note=struct('declared_before_native_outcomes',char(datetime('now')),'source_protocol','Final V5 comparison protocol already frozen; native eight-second ES added with identical seeds/configurations. Main comparison outcomes existed before this extension; no settings selected from them.','duration_s',8,'seeds',P.seeds,'conditions',P.conditions);
fid=fopen(fullfile(folder,'protocol.json'),'w');fprintf(fid,'%s',jsonencode(note,PrettyPrint=true));fclose(fid);rows=struct([]);tic;
for condition=P.conditions
 c=P.config;c.dwells=.36;c.esDuration=8;c.noise=c.noise*condition.noise;c.powerNoise=c.powerNoise*condition.noise;c.sensorBias=[condition.bias;-.5*condition.bias]*1e-6;c.actualAlphaFactor=condition.beam;
 L=v4_library(c);legacy=v3_designs(c);
 for name=P.scenarios
  traces=cell(numel(P.seeds),1);passiveTraces=traces;
  for i=1:numel(P.seeds)
   p=v5_trial(name{1},P.seeds(i),'passive',c,L,legacy);r=v5_trial(name{1},P.seeds(i),'lockin',c,L,legacy,p.trace);
   traces{i}=r.trace;passiveTraces{i}=p.trace;r=rmfield(r,'trace');r.method='lockin_native';r.condition=condition.name;r.Jfactor=0;r.taufactor=0;
   if isempty(rows),rows=r;else,rows(end+1)=r;end
  end
  save(fullfile(folder,sprintf('trial_%s_%s.mat',condition.name,name{1})),'traces','passiveTraces','c','-v7');
 end
 fprintf('Native ES %s: %d rows %.1fs\n',condition.name,numel(rows),toc);
end
writetable(struct2table(rows),fullfile(folder,'native.csv'));
end
