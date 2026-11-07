function export_actuator_reference
[here,~]=v5_setup;c=v4_config;c.esDuration=2.88;
L=v4_library(c);AD=zeros(4,4,6);BD=zeros(4,3,6);m=0;
for jf=c.Jfactors
 for tf=c.taufactors
  m=m+1;[AD(:,:,m),BD(:,:,m)]=pid_discrete(c,jf,tf);
 end
end
availability=struct('CORA_reach',exist('reach','file'),'CORA_interval',exist('interval','class'),...
 'YALMIP_sdpvar',exist('sdpvar','file'),'Gurobi',exist('gurobi','file'));
save(fullfile(here,'results','verification','actuator_reference.mat'),'c','L','AD','BD','availability','-v7');
end
