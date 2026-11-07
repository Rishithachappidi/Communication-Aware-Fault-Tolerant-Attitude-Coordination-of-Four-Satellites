function search_frontiers
[here,~]=v6_setup;folder=fullfile(here,'results','development');assert(~isfolder(folder));mkdir(folder);
% Deterministic measured-state design map, not simulation performance selection.
% Sets and transition-selection rules written before map outcomes.
P=struct('noiseScales',[.25 .5 .75 1 1.25 1.5 2],...
 'powerRatios',1:.005:2.2,'gainBounds',[0 .045 .09 .15],...
 'currentAngle',zeros(2,1),'selection','For each noise/gain-bound, record every change of (UAD admission, fixed-margin admission). Confirm both sides of every such transition on new seed7001:7100; do not select only favorable outcomes. The map uses measured state and no unknown injection truth.');
fid=fopen(fullfile(folder,'protocol.json'),'w');fprintf(fid,'%s',jsonencode(P,PrettyPrint=true));fclose(fid);
rows=struct([]);transitions=struct([]);
for ns=P.noiseScales
 for bound=P.gainBounds
  c=v4_config;c.esDuration=2.88;c.dwells=.36;c.noise=c.noise*ns;c.powerNoise=c.powerNoise*ns;c.driftBound=bound;
  L=v4_library(c);prev=[];
  for ratio=P.powerRatios
   pm=ratio*c.sensitivity;u=uad_plan(pm,[0;0],c,L);g=guarded_plan(pm,[0;0],c,L);
   r=struct('noise_scale',ns,'drift_bound',bound,'power_ratio',ratio,'UAD_admit',u.ok,'guard_admit',g.ok,'UAD_risk',u.riskSeconds,'guard_risk',g.riskSeconds);
   if isempty(rows),rows=r;else,rows(end+1)=r;end
   now=[u.ok g.ok];
   if ~isempty(prev)&&~isequal(now,prev)
    for val=[ratio-.005 ratio]
     z=struct('noise_scale',ns,'drift_bound',bound,'power_ratio',val,'from_UAD',prev(1),'from_guard',prev(2),'to_UAD',now(1),'to_guard',now(2));
     if isempty(transitions),transitions=z;else,transitions(end+1)=z;end
    end
   end
   prev=now;
  end
 end
end
writetable(struct2table(rows),fullfile(folder,'admission_map.csv'));writetable(struct2table(transitions),fullfile(folder,'transitions.csv'));
save(fullfile(folder,'map.mat'),'rows','transitions','P','-v7');disp(transitions);
end
