function audit_v4_raw
[here,~]=v4_setup;folder=fullfile(here,'results','final');load(fullfile(folder,'protocol.mat'),'P');
primary=readtable(fullfile(folder,'primary_corrected.csv'));sensitivity=readtable(fullfile(folder,'sensitivity_corrected.csv'));
report=struct('status','running','primary_traces',0,'sensitivity_traces',0,'counterfactuals_regenerated',0,'mat_files',0);tic;
for name=P.scenarios
 x=load(fullfile(folder,['primary_' name{1} '.mat']),'traces','c');
 mask=strcmp(primary.scenario,name{1});rows=primary(mask,:);
 for i=1:numel(P.primarySeeds)
  passive=x.traces{i,1};
  for j=1:numel(P.methods)
   row=rows(rows.seed==P.primarySeeds(i)&strcmp(rows.method,P.methods{j}),:);
   verify(x.traces{i,j},row,x.c,passive);report.primary_traces=report.primary_traces+1;
  end
 end
 report.mat_files=report.mat_files+1;fprintf('Raw audit primary %s %.1fs\n',name{1},toc);
end
for sweep=P.sweeps
 for value=sweep.values
  for name=sweep.scenarios
   file=sprintf('sensitivity_%s_%g_%s.mat',sweep.name,value,name{1});x=load(fullfile(folder,file),'traces','c');
   mask=strcmp(sensitivity.condition,sweep.name)&sensitivity.condition_value==value&strcmp(sensitivity.scenario,name{1});rows=sensitivity(mask,:);
   L=v4_library(x.c);legacy=v3_designs(x.c);passiveDown=false(numel(x.traces{1,1}.t),numel(P.sensitivitySeeds));
   for i=1:numel(P.sensitivitySeeds)
    p=v4_trial(name{1},P.sensitivitySeeds(i),'passive',x.c,L,legacy);passive=p.trace;
    passiveDown(:,i)=passive.down;report.counterfactuals_regenerated=report.counterfactuals_regenerated+1;
    for j=1:numel(sweep.methods)
     row=rows(rows.seed==P.sensitivitySeeds(i)&strcmp(rows.method,sweep.methods{j}),:);
     verify(x.traces{i,j},row,x.c,passive);report.sensitivity_traces=report.sensitivity_traces+1;
    end
   end
   % Preserve the missing passive masks needed to reconstruct sensitivity causal metrics.
   save(fullfile(folder,['counterfactual_' file]),'passiveDown','-v7');
   report.mat_files=report.mat_files+1;
  end
  fprintf('Raw audit sensitivity %s %g %.1fs\n',sweep.name,value,toc);
 end
end
report.status='passed';report.elapsed_s=toc;
fid=fopen(fullfile(folder,'raw_audit.json'),'w');fprintf(fid,'%s',jsonencode(report,PrettyPrint=true));fclose(fid);disp(report);
end
function verify(z,row,c,passive)
assert(height(row)==1);t=z.t;eval=t>=2;down=z.power<c.sensitivity;
assert(isequal(down,z.down));assert(abs(sum(down(eval))*c.dt-row.outage_s)<1e-10);
assert(abs(sum(z.probe)*c.dt-row.probe_s)<1e-10);
assert(abs(sum(z.angle(z.probe,:).^2,'all')*c.dt*1e12-row.energy_urad2s)<1e-8);
assert(abs(sum(down(eval)&~passive.down(eval))*c.dt-row.probe_induced_outage_s)<1e-10);
if ~isempty(z.fit),assert(double(z.fit.ok)==row.accepted);end
has=isfinite(z.lower);bv=any(z.power(has)+1e-14<z.lower(has));assert(double(bv)==row.bound_violation);
if any(has)
 first=find(z.probe,1);last=find(z.probe,1,'last');q0=z.angle(first,:);
 tv=any(vecnorm(z.angle(has,:)-q0-z.motion(has,:),2,2)>z.tube(has)+1e-12);assert(double(tv)==row.tube_violation);
 [bfirst,~]=v4_truth(t(first),row.scenario{1},row.seed,c);[blast,~]=v4_truth(t(last),row.scenario{1},row.seed,c);
 constant=norm(bfirst-blast)<1e-15;
 if row.certificate_premises_recorded&&~constant,assert(~row.certificate_premises);end
end
if row.accepted
 [b,~]=v4_truth(t(end),row.scenario{1},row.seed,c);
 assert(abs(norm(z.fit.b-b)*1e6-row.accepted_error_um)<1e-8);
 assert(double(norm(z.fit.b-b)<=z.fit.radius)==row.coverage_all_fits);
end
end
