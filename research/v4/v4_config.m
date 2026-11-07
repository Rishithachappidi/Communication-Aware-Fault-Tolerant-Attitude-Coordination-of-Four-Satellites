function c=v4_config
c=v3_config;c.version='4.0';c.delta=0.01;c.alphaRange=c.alpha*[0.9 1.1];
c.p0Range=[optical_power([0;0],1,false,setfield(c,'divergence',c.alphaRange(2))) ...
 optical_power([0;0],1,false,setfield(c,'divergence',c.alphaRange(1)))]; %#ok<SFLD>
c.gainMax=1.05;c.kappa=sqrt(2)*erfcinv(c.delta/(5*ceil(c.T/c.dt)));
c.amplitudes=[2 4 6 8]*1e-6;c.dwells=[0.36 0.5];
c.Jfactors=[0.8 1 1.25];c.taufactors=[1 1.5];
c.fitAlpha=0.01;c.maxFitIterations=12;c.esGain=0.3;c.kfProcess=0;
c.actualJfactor=1;c.actualTaufactor=1;c.actualAlphaFactor=1;
c.sensorBias=[0;0];c.driftSlope=0.09;c.curvature=0.008;
c.fadingAmplitude=0.16;c.nearGain=0.41;c.offsetScale=1;
c.fitDegree=1;c.libraryLimit=Inf;c.serviceBudget=0;c.acquisitionBudget=4;
end
