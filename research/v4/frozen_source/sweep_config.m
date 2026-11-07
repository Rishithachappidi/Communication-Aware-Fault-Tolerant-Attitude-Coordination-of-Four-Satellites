function c=sweep_config(c,name,value)
switch name
 case 'noise',c.noise=c.noise*value;c.powerNoise=c.powerNoise*value;
 case 'slope',c.driftSlope=value;
 case 'curvature',c.curvature=value;
 case 'fading',c.fadingAmplitude=value;
 case 'beam',c.actualAlphaFactor=value;
 case 'offset',c.offsetScale=value;
 case 'actuator'
  factors=[0.8 1;1.25 1.5;1.5 2];c.actualJfactor=factors(value,1);c.actualTaufactor=factors(value,2);
 case 'bias',c.sensorBias=[value;-value/2]*1e-6;
 case 'margin',c.nearGain=value;
 case 'library',c.libraryLimit=value;
 case 'confidence',c.delta=value;c.noise=c.noise*5;c.powerNoise=c.powerNoise*5;
 case 'budget',c.serviceBudget=value;
 case 'half_step',c.dt=c.dt*value;
 otherwise,error('Unknown sweep');
end
c.kappa=sqrt(2)*erfcinv(c.delta/(5*ceil(c.T/c.dt)));
end
