function P=v5_protocol
P=struct;P.config=v4_config;P.config.esDuration=2.88;
P.seeds=5001:5050;P.actuatorSeeds=6001:6020;
P.scenarios={'healthy','pointing','linear_drift','attenuation_only','quadratic_drift','fast_fading','deep_loss','near_threshold','dark'};
P.methods={'DAP','UAD','guarded','lockin'};
P.conditions=struct('name',{'nominal','noise5','bias2','early_fault'},'noise',{1,5,1,1},'bias',{0,0,2,0},'beam',{1,1,1,.9});
P.budget='All library candidates restricted to eight 0.36-s dwells (2.88 s). ES runs exactly 2.88 s after shared trigger; shared command norm clamp 35 urad (realized amplitudes need not match). Report realized angular energy; energy is not claimed matched. Native V4 ES eight-second results stay separate.';
P.guard='Fixed 2-urad delivered-motion margin plus current encoder envelope, selected before new outcomes; no impulse enclosure or universal robustness theorem.';
P.actuatorJ=[.8 .91 1 1.13 1.25];P.actuatorTau=[1 1.12 1.25 1.37 1.5];
P.actuatorScenarios={'linear_drift','near_threshold'};P.actuatorMethods={'UAD','guarded','lockin'};
P.outOfModel='Interior actuator grid points are stress tests, never certified by a finite endpoint argument. Bias and faults during probing remain outside static unbiased hypotheses.';
end
