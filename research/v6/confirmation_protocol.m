function P=confirmation_protocol
[here,~]=v6_setup;d=readtable(fullfile(here,'results','development','admission_map.csv'));
P=struct;P.seeds=7001:7100;P.methods={'UAD','guarded'};P.J=[.8 1 1.25];P.tau=[1 1.5];P.config=v4_config;P.config.esDuration=2.88;P.config.dwells=.36;
P.selection='After deterministic admission-map exploration, before any new confirmation simulation: choose lexicographically first noise/gain-bound group containing each disagreement direction, then band midpoint and the adjacent grid points below/above. Retain both directions and all controls, even when unreachable after the causal trigger.';
P.development_amendment='The development protocol originally suggested confirming every transition. Confirmation narrows this to the first representative band in each direction with surrounding controls, to test mechanism and causal reachability instead of repeatedly measuring the same frontier. All 6748 map rows retained. No confirmation simulation outcomes existed when this choice was frozen.';
P.scope='Exploratory, development-guided mechanism study. Not an untouched global superiority test. Original 2800 identical V5 pairs remain unchanged.';
P.cases=struct([]);
for direction=1:2
 if direction==1,mask=d.UAD_admit==1&d.guard_admit==0;else,mask=d.UAD_admit==0&d.guard_admit==1;end
 a=d(mask,:);a=sortrows(a,{'noise_scale','drift_bound','power_ratio'});assert(~isempty(a));ns=a.noise_scale(1);bound=a.drift_bound(1);
 a=a(a.noise_scale==ns&a.drift_bound==bound,:);lo=min(a.power_ratio);hi=max(a.power_ratio);
 values=[lo-.005 (lo+hi)/2 hi+.005];labels={'below','middle','above'};
 for i=1:3
  x=struct('id',sprintf('direction%d_%s',direction,labels{i}),'direction',direction,'position',labels{i},'noise_scale',ns,'drift_bound',bound,'power_ratio',values(i));
  if isempty(P.cases),P.cases=x;else,P.cases(end+1)=x;end
 end
end
end
