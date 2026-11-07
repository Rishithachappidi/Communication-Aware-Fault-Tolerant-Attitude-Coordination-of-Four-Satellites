function report=test_v5
v5_setup;c=v4_config;c.esDuration=2.88;c.dwells=.36;L=v4_library(c);legacy=v3_designs(c);
a=v4_trial('linear_drift',123,'UAD',c,L,legacy);b=v5_trial('linear_drift',123,'UAD',c,L,legacy);
assert(isequal(a.trace.power,b.trace.power));assert(isequal(a.trace.angle,b.trace.angle));
p=v5_trial('linear_drift',123,'passive',c,L,legacy);
e=v5_trial('linear_drift',123,'lockin',c,L,legacy,p.trace);assert(abs(e.probe_s-2.88)<1e-10);assert(~e.accepted);
g=v5_trial('linear_drift',123,'guarded',c,L,legacy,p.trace);
assert(g.probe_s<=2.88+1e-9);assert(isequal(g.trace.standardized_noise,e.trace.standardized_noise));
assert(isequal(size(g.trace.offset_truth),[700 2]));
report=struct('status','passed','checks',{{'V4/V5 UAD trajectory equivalence','ES time-matched cap and no diagnosis credit','fixed guard time cap','paired exogenous disturbances','truth/noise logging dimensions'}});disp(report);
end
