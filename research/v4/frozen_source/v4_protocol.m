function P=v4_protocol
% Complete experiment declaration; outcome-independent final seed lists.
P=struct;P.config=v4_config;
P.scenarios={'healthy','pointing','linear_drift','attenuation_only','quadratic_drift','fast_fading','deep_loss','near_threshold','dark'};
P.methods={'passive','constant_fit','projected_fixed','balanced_fixed','no_service','DAP',...
 'projected_noise','parameter_kf','lockin','UAD','UAD_no_tube','UAD_point_gate'};
P.primarySeeds=3001:3100;P.sensitivitySeeds=4001:4050;
P.sensitivityMethods={'projected_fixed','DAP','projected_noise','parameter_kf','lockin','UAD'};
P.sweeps=struct([]);
P=add(P,'noise',{'pointing','linear_drift','near_threshold'},[1 2 5 10]);
P=add(P,'slope',{'linear_drift'},[0 0.045 0.09 0.15 0.25]);
P=add(P,'curvature',{'quadratic_drift'},[0.004 0.008 0.02]);
P=add(P,'fading',{'fast_fading'},[0.04 0.16 0.3]);
P=add(P,'beam',{'pointing','linear_drift'},[0.9 1 1.1 1.2]);
P=add(P,'offset',{'pointing','linear_drift'},[0.5 1 1.2]);
P=add(P,'actuator',{'linear_drift','near_threshold'},[1 2 3]);
P=add(P,'bias',{'linear_drift','near_threshold'},[0 0.5 2]);
P=add(P,'margin',{'near_threshold'},[0.385 0.41 0.5 0.7]);
P=add(P,'library',{'linear_drift'},[2 4 8],{'UAD','UAD_no_tube'});
P=add(P,'confidence',{'near_threshold'},[0.001 0.01 0.1],{'UAD','UAD_point_gate'});
P=add(P,'budget',{'near_threshold'},[0 0.5 1 2 4],{'DAP','UAD','UAD_no_tube'});
P=add(P,'half_step',{'linear_drift','near_threshold'},[1 0.5]);
P.baselineDevelopment='seeds41:45, nine scenarios, noise1/5; ES gains0.1/0.3/0.6, KF processes0/1e-4/0.01';
P.baselineSelection='minimum mean outage across all development conditions, false-correction count tie-break, lower value final tie-break';
P.selectedBaseline=struct('esGain',0.3,'kfProcess',0);
P.statisticalUnit='seed, paired within scenario/config; no time-sample replication';
P.raw='All main/sensitivity measurement/power/angle/probe/certificate arrays retained in per-condition MAT chunks';
end
function P=add(P,name,scenarios,values,methods)
if nargin<5,methods=P.sensitivityMethods;end
s=struct('name',name,'scenarios',{scenarios},'values',values,'methods',{methods});
if isempty(P.sweeps),P.sweeps=s;else,P.sweeps(end+1)=s;end
end
