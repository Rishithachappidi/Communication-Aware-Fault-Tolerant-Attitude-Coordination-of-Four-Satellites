function run_confirmation
[here,root]=v6_setup;folder=fullfile(here,'results','confirmation');assert(~isfolder(folder));mkdir(folder);P=confirmation_protocol;
fid=fopen(fullfile(folder,'protocol.json'),'w');fprintf(fid,'%s',jsonencode(P,PrettyPrint=true));fclose(fid);save(fullfile(folder,'protocol.mat'),'P','-v7');
files=[dir(fullfile(here,'*.m'));dir(fullfile(root,'research','v5','*.m'));dir(fullfile(root,'research','v4','*.m'));dir(fullfile(root,'research','v3','*.m'))];H=struct;
for i=1:numel(files)
 p=fullfile(files(i).folder,files(i).name);md=java.security.MessageDigest.getInstance('SHA-256');md.update(uint8(fileread(p)));
 H.(matlab.lang.makeValidName(strrep(p,[root filesep],'')))=lower(reshape(dec2hex(typecast(md.digest(),'uint8'),2)',1,[]));
end
fid=fopen(fullfile(folder,'source_sha256.json'),'w');fprintf(fid,'%s',jsonencode(H,PrettyPrint=true));fclose(fid);
rows=struct([]);tic;
for specification=P.cases
 c=P.config;c.noise=c.noise*specification.noise_scale;c.powerNoise=c.powerNoise*specification.noise_scale;c.driftBound=specification.drift_bound;c.nearGain=specification.power_ratio*c.sensitivity/c.p0;
 L=v4_library(c);legacy=v3_designs(c);
 for jf=P.J
  for tf=P.tau
   c.actualJfactor=jf;c.actualTaufactor=tf;traces=cell(numel(P.seeds),2);passiveTraces=cell(numel(P.seeds),1);
   for i=1:numel(P.seeds)
    p=v6_trial('near_threshold',P.seeds(i),'passive',c,L,legacy);passiveTraces{i}=p.trace;
    for j=1:2
     r=v6_trial('near_threshold',P.seeds(i),P.methods{j},c,L,legacy,p.trace);traces{i,j}=r.trace;r=rmfield(r,'trace');r.case_id=specification.id;r.condition='frontier';r.Jfactor=jf;r.taufactor=tf;
     if isempty(rows),rows=r;else,rows(end+1)=r;end
    end
   end
   save(fullfile(folder,sprintf('trace_%s_J%g_T%g.mat',specification.id,jf,tf)),'traces','passiveTraces','c','specification','-v7');
  end
 end
 fprintf('Confirmation %s: %d rows %.1fs\n',specification.id,numel(rows),toc);
end
writetable(struct2table(rows),fullfile(folder,'trials.csv'));
end
