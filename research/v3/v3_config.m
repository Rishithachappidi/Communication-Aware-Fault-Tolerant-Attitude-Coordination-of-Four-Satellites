function c=v3_config
% Research protocol constants fixed before the evaluation batch.
c=default_config(4);c.controller='PID';c.dt=0.02;c.T=14;
c.p0=optical_power([0;0],1,false,c);c.alpha=c.divergence;
c.sigma=0.03;c.targetRadius=1e-6;c.maxResidual=0.06;
c.priorRadius=30e-6;c.driftBound=0.15;c.serviceBudget=0;
c.acquisitionBudget=4;c.detectLog=0.18;c.offsetThreshold=4e-6;
c.detectionCount=3;c.settleFraction=0.6;c.probeStart=NaN;
end
