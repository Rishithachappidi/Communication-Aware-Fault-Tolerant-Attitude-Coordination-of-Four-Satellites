function [b,g]=v3_truth(t,name,seed)
% Injection/evaluation only. Never passed to fit or planning functions.
b=zeros(2,1);g=1;if t<2,return;end
angle=0.4+0.9*sin(seed);b0=(20+6*cos(seed))*1e-6*[cos(angle);sin(angle)];
switch name
 case 'healthy'
 case 'pointing',b=b0;
 case 'linear_drift',b=b0;g=exp(-0.09*(t-2));
 case 'attenuation_only',g=exp(-0.09*(t-2));
 case 'quadratic_drift',b=b0;g=exp(-0.008*(t-2)^2);
 case 'fast_fading',b=b0;g=exp(-0.045*(t-2)+0.16*sin(4*(t-2)));
 case 'deep_loss',b=b0;g=0.18;
 case 'near_threshold',g=0.41;
 case 'dark',g=0;
 otherwise,error('Unknown injection');
end
end
