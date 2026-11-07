function develop_baselines
v4_setup;here=fileparts(mfilename('fullpath'));rows=struct([]);
c=v4_config;L=v4_library(c);legacy=v3_designs(c);
for method={'lockin','parameter_kf'}
 grid=[0.1 0.3 0.6];if strcmp(method{1},'parameter_kf'),grid=[0 1e-4 1e-2];end
 for value=grid
  cc=c;if strcmp(method{1},'lockin'),cc.esGain=value;else,cc.kfProcess=value;end
  for noise=[1 5]
   dc=cc;dc.noise=noise*c.noise;dc.powerNoise=noise*c.powerNoise;
   for name={'healthy','pointing','linear_drift','attenuation_only','quadratic_drift','fast_fading','deep_loss','near_threshold','dark'}
    for seed=41:45
     r=v4_trial(name{1},seed,method{1},dc,L,legacy);r=rmfield(r,'trace');
     r.development_value=value;r.noise_factor=noise;
     if isempty(rows),rows=r;else,rows(end+1)=r;end
    end
   end
  end
 end
end
T=struct2table(rows);writetable(T,fullfile(here,'results','baseline_development.csv'));
for method={'lockin','parameter_kf'}
 vals=unique(T.development_value(strcmp(T.method,method{1})));
 for val=vals'
  X=T(strcmp(T.method,method{1})&T.development_value==val,:);
  fprintf('%s value %.4g meanOutage %.5f falseCorrections %d accepted %d\n',method{1},val,mean(X.outage_s),sum(X.false_correction),sum(X.accepted));
 end
end
end
