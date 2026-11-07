function [lo,hi,mode]=power_envelope(pm,c)
% Simultaneous mission-wise Gaussian marginal envelope via a union bound.
eta=c.kappa*c.powerNoise;lo=0;hi=Inf;mode='uncertain';
if ~isfinite(pm) || pm<0 || eta>=1,return;end
lo=pm/(1+eta);hi=pm/(1-eta);
if hi<c.sensitivity,mode='acquisition';elseif lo>=c.sensitivity,mode='service';end
end
