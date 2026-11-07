function [b,g]=v4_truth(t,name,seed,c)
% Injection and evaluation only. Config is not handed to the estimator wholesale.
[b,g]=v3_truth(t,name,seed);if t<2,return;end
b=b*c.offsetScale;
switch name
 case {'linear_drift','attenuation_only'},g=exp(-c.driftSlope*(t-2));
 case 'quadratic_drift',g=exp(-c.curvature*(t-2)^2);
 case 'fast_fading',g=exp(-0.045*(t-2)+c.fadingAmplitude*sin(4*(t-2)));
 case 'near_threshold',g=c.nearGain;
end
end
