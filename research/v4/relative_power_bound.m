function [lower,D]=relative_power_bound(pLower,elapsed,d,rad,center,R,alphaLower,L)
% Conditional bound for e0 in ball(center,R), delivered increment in ball(d,rad).
% Every rad is a 2-norm radius, not a per-axis standard deviation.
assert(pLower>=0 && R>=0 && all(rad>=0) && alphaLower>0 && L>=0);
D=2*d*center(:)+2*R*vecnorm(d,2,2)+sum(d.^2,2) ...
 +2*(vecnorm(d+center(:)',2,2)+R).*rad+rad.^2;
% Negative worst-case losses are conservatively replaced by zero when alpha is uncertain.
lower=pLower*exp(-L*elapsed-2*max(D,0)/alphaLower^2);
end
