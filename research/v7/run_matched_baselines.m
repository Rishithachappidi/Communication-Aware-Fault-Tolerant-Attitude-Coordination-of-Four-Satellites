function run_matched_baselines
[here,root]=v7_setup;folder=fullfile(here,'results','matched_baselines');assert(~isfolder(folder));mkdir(folder);
old=load(fullfile(root,'research','v6','results','confirmation','protocol.mat'),'P');P=old.P;
P.methods={'parameter_kf','lockin'};P.sigmaRateGain=2;P.sigmaRateGainUnit='s^-1';
P.extension='Frozen before this baseline extension, after the original two-selector confirmation outcomes. Same six settings,100 seeds and six finite actual models; 2.88-second time budget for parameter KF and ES. Neither complete published chance-AFD nor safety-filtered ES is claimed reproduced.';
fid=fopen(fullfile(folder,'protocol.json'),'w');fprintf(fid,'%s',jsonencode(P,PrettyPrint=true));fclose(fid);save(fullfile(folder,'protocol.mat'),'P','-v7');
paths=[dir(fullfile(here,'*.m'));dir(fullfile(root,'research','v6','*.m'));dir(fullfile(root,'research','v5','*.m'));dir(fullfile(root,'research','v4','*.m'));dir(fullfile(root,'research','v3','*.m'))];H=struct;
for k=1:numel(paths)
 p=fullfile(paths(k).folder,paths(k).name);md=java.security.MessageDigest.getInstance('SHA-256');md.update(uint8(fileread(p)));H.(matlab.lang.makeValidName(strrep(p,[root filesep],'')))=lower(reshape(dec2hex(typecast(md.digest(),'uint8'),2)',1,[]));
end
fid=fopen(fullfile(folder,'source_sha256.json'),'w');fprintf(fid,'%s',jsonencode(H,PrettyPrint=true));fclose(fid);
rows=struct([]);tic;
for specification=P.cases
 c=P.config;c.noise=c.noise*specification.noise_scale;c.powerNoise=c.powerNoise*specification.noise_scale;c.driftBound=specification.drift_bound;c.nearGain=specification.power_ratio*c.sensitivity/c.p0;
 c.rateNoise=2*c.noise;c.rateNoiseUnit='rad/s';c.angleNoiseUnit='rad';
 L=v4_library(c);legacy=v3_designs(c);
 for jf=P.J
  for tf=P.tau
   c.actualJfactor=jf;c.actualTaufactor=tf;traces=cell(numel(P.seeds),2);passiveTraces=cell(numel(P.seeds),1);
   for i=1:numel(P.seeds)
    p=v6_trial('near_threshold',P.seeds(i),'passive',c,L,legacy);passiveTraces{i}=p.trace;
    for j=1:2
     r=v6_trial('near_threshold',P.seeds(i),P.methods{j},c,L,legacy,p.trace);
     % Additional explicit unit metadata; no change to inherited sensor values.
     r.trace.measured_rate=r.trace.state_history(:,3:4)+c.rateNoise*r.trace.standardized_noise(:,3:4);
     traces{i,j}=r.trace;r=rmfield(r,'trace');r.case_id=specification.id;r.condition='frontier';r.Jfactor=jf;r.taufactor=tf;
     if isempty(rows),rows=r;else,rows(end+1)=r;end
    end
   end
   save(fullfile(folder,sprintf('trace_%s_J%g_T%g.mat',specification.id,jf,tf)),'traces','passiveTraces','c','specification','-v7');
  end
 end
 fprintf('Matched baselines %s: %d runs %.1fs\n',specification.id,numel(rows),toc);
end
writetable(struct2table(rows),fullfile(folder,'trials.csv'));
end
