function r=v6_trial(name,seed,method,c,lib,legacy,passive)
% All decisions use a whitelisted nominal config, measured q,p, and stored history.
% Hidden injection is confined to plant construction and evaluator quantities.
if nargin<7,passive=[];end
dc=decision_config(c);rng(seed,'twister');t=(0:c.dt:c.T-c.dt)';N=numel(t);Z=randn(N,5);
actual=c;actual.divergence=c.alpha*c.actualAlphaFactor;p=terminal_parameters(c);
p(12)=optical_power([0;0],1,false,actual);p(16)=actual.divergence;
x=zeros(8,1);ref=zeros(2,1);power=zeros(N,1);qm=zeros(N,2);pm=zeros(N,1);
stateHistory=zeros(N,8);referenceHistory=zeros(N,2);angle=zeros(N,2);gainTruth=zeros(N,1);offsetTruth=zeros(N,2);probe=false(N,1);command=zeros(N,2);lower=nan(N,1);motion=nan(N,2);tube=nan(N,1);
active=false;attempted=false;accepted=false;refused=false;fitRejected=false;
start=NaN;finish=NaN;count=0;indices=[];fit=[];qstart=zeros(2,1);qstartTrue=qstart;
fitB=[NaN;NaN];correction=zeros(2,1);plan=[];esMean=0;esGrad=zeros(2,1);esCenter=zeros(2,1);
diagnosis_s=NaN;planRuntime=0;fitRuntime=0;fitGain=NaN;
[S,~]=dap_sequences;
for k=1:N
 stateHistory(k,:)=x';now=t(k);[b,g]=v4_truth(now,name,seed,c);gainTruth(k)=g;offsetTruth(k,:)=b';
 u=[ref;1;1;g;0;c.sensorBias;b;1];[~,y]=v4_kernel(x,u,Z(k,:)',p,c);o=sensor_view(y);
 power(k)=y(16);angle(k,:)=y(3:4)';qm(k,:)=o.angle';pm(k)=o.power;
 nominal=dc.p0*exp(-2*sum(o.angle.^2)/dc.alpha^2);
 anomaly=abs(log(max(o.power,0.0001*dc.p0)/max(nominal,0.0001*dc.p0)))>dc.detectLog;
 if now>1 && anomaly,count=count+1;else,count=0;end
 if count>=dc.detectionCount && ~attempted && ~strcmp(method,'passive')
  attempted=true;qstart=o.angle;qstartTrue=y(3:4);tick=tic;
  plan=struct('ok',false,'q',6e-6*S(:,:,2),'dwell',0.36,'amplitude',6e-6,...
   'riskSeconds',NaN,'mode','unconstrained','lower',[],'motion',[],'tube',[]);
  if o.power<=0.005*dc.p0
   plan.ok=false;
  elseif any(strcmp(method,{'UAD','guarded','UAD_no_tube','UAD_point_gate'}))
   variant='UAD';if strcmp(method,'UAD_no_tube'),variant='no_tube';end
   if strcmp(method,'UAD_point_gate'),variant='point_gate';end
   if strcmp(method,'guarded'),plan=guarded_plan(o.power,o.angle,dc,lib);else,plan=uad_plan(o.power,o.angle,dc,lib,variant);end
  elseif any(strcmp(method,{'DAP','no_service'}))
   p3=dap_plan(o.power,dc,legacy,strcmp(method,'DAP'));
   plan.ok=p3.ok;plan.q=p3.q;plan.dwell=p3.dwell;plan.amplitude=p3.amplitude;
   plan.riskSeconds=p3.riskSeconds;plan.mode='service';if o.power<dc.sensitivity,plan.mode='acquisition';end
  else
   plan.ok=true;if strcmp(method,'balanced_fixed'),plan.q=6e-6*S(:,:,1);end
  end
  planRuntime=toc(tick);
  if plan.ok,active=true;start=now;else,refused=true;end
 end
 if active
  age=now-start;duration=8*plan.dwell;
  if strcmp(method,'lockin'),duration=dc.esDuration;end
  if age<duration-1e-9
   probe(k)=true;
   if strcmp(method,'lockin')
    % Standard two-channel washout/demodulation/integral extremum-seeking adaptation.
    val=log(max(o.power,0.005*dc.p0)/dc.p0);
    if age==0,esMean=val;end
    esMean=esMean+dc.dt*(val-esMean);osc=sin(2*pi*[0.25;0.4]*age);
    demod=2/4e-6*(val-esMean)*osc;
    esGrad=esGrad+0.7*dc.dt*(demod-esGrad);
    esCenter=clip(esCenter+dc.esGain*dc.dt*dc.alpha^2/4*esGrad,dc.maxCorrection-4e-6);
    ref=clip(esCenter+4e-6*osc,dc.maxCorrection);
   else
    phase=min(8,floor((age+1e-9)/plan.dwell)+1);ref=plan.q(phase,:)';
   end
   if mod(age+1e-9,plan.dwell)>=dc.settleFraction*plan.dwell,indices(end+1)=k;end
   if ~isempty(plan.lower)
    j=min(numel(plan.lower),round(age/dc.dt)+1);lower(k)=plan.lower(j);
    motion(k,:)=plan.motion(j,:)-qstart';tube(k)=plan.tube(j);
   end
  else
   active=false;finish=now;tick=tic;
   degree=1;if strcmp(method,'constant_fit'),degree=0;end
   if strcmp(method,'lockin')
    fitB=-esCenter;correction=esCenter;ref=correction; % Tracker: no certified fault diagnosis.
   else
    if strcmp(method,'parameter_kf')
     fit=parameter_kf_fit(t(indices),qm(indices,:),pm(indices),dc);
    elseif strcmp(method,'ekf')
     fit=joint_ekf_fit(t(indices),qm(indices,:),pm(indices),dc);
    elseif any(strcmp(method,{'projected_noise','UAD','guarded','UAD_no_tube','UAD_point_gate'}))
     fit=noise_aware_fit(t(indices),qm(indices,:),pm(indices),dc,dc.fitDegree);
    else,fit=dap_fit(t(indices),qm(indices,:),pm(indices),dc,degree);end
    fitB=fit.b;fitGain=fit.gain;accepted=fit.ok;fitRejected=~fit.ok;
    if any(strcmp(fit.reason,{'rank','temporal-rank','censored','insufficient-data'})),fitB=[NaN;NaN];end
    if accepted
     diagnosis_s=now;
     opticalGood=dc.p0*fit.gain>1.05*dc.sensitivity;
     pointingGood=norm(fit.b)>dc.offsetThreshold;
     if any(strcmp(method,{'projected_noise','UAD','guarded','UAD_no_tube','UAD_point_gate','ekf','parameter_kf'}))
      opticalGood=dc.p0*exp(log(fit.gain)-2.576*fit.gainSE)>1.05*dc.sensitivity;
      pointingGood=norm(fit.b)-fit.radius>dc.offsetThreshold;
     end
     if opticalGood && pointingGood,correction=clip(-fit.b,dc.maxCorrection);end
    end
    ref=correction;
   end
   fitRuntime=toc(tick);
  end
 end
 % Causal held reference is used for the next integration interval; log that interval's torque.
 referenceHistory(k,:)=ref';u(1:2)=ref;[~,yy]=v4_kernel(x,u,Z(k,:)',p,c);command(k,:)=yy(11:12)';
 x=v4_advance(x,u,Z(k,:)',p,c);
end
eval=t>=2;tail=t>=12;down=power<c.sensitivity;[bEnd,gEnd]=v4_truth(t(end),name,seed,c);
err=NaN;coverage=NaN;radius=NaN;
if all(isfinite(fitB)),err=norm(fitB-bEnd)*1e6;end
if ~isempty(fit),radius=fit.radius;coverage=double(norm(fit.b-bEnd)<=fit.radius);end
acceptedError=NaN;if accepted,acceptedError=err;end
attemptError=NaN;if attempted,attemptError=err;end
probeInduced=NaN;avoided=NaN;
if ~isempty(passive),probeInduced=sum(down(eval)&~passive.down(eval))*c.dt;avoided=sum(~down(eval)&passive.down(eval))*c.dt;end
boundMask=isfinite(lower);boundViolation=any(power(boundMask)+1e-14<lower(boundMask));
tubeViolation=false;if any(boundMask),tubeViolation=any(vecnorm(angle(boundMask,:)-qstartTrue'-motion(boundMask,:),2,2)>tube(boundMask)+1e-12);end
falseAcq=false;budgetViolation=false;predicted=NaN;mode='none';
if ~isempty(plan)
 mode=plan.mode;predicted=plan.riskSeconds;
 if any(probe)
  first=find(probe,1);falseAcq=strcmp(mode,'acquisition') && power(first)>=c.sensitivity;
  budget=c.serviceBudget;if strcmp(mode,'acquisition'),budget=c.acquisitionBudget;end
  if ~isnan(predicted),budgetViolation=sum(down&probe)*c.dt>budget+1e-9;end
 end
end
stateVars=whos('power','angle','qm','pm','command','probe','lower','motion','tube','Z','t');traceBytes=sum([stateVars.bytes]);
certified=any(boundMask);premises=false;
if certified
 first=find(probe,1);gainOK=all(gainTruth(probe)>=gainTruth(first)*exp(-c.driftBound*(t(probe)-t(first)))-1e-12);
 member=any(abs(c.Jfactors-c.actualJfactor)<1e-10)&&any(abs(c.taufactors-c.actualTaufactor)<1e-10);
 beamOK=actual.divergence>=c.alphaRange(1)&&actual.divergence<=c.alphaRange(2);
 [bFirst,~]=v4_truth(t(first),name,seed,c);last=find(probe,1,'last');
 [bLast,~]=v4_truth(t(last),name,seed,c);constantOffset=all(vecnorm(offsetTruth(probe,:)-bFirst',2,2)<1e-15);
 premises=constantOffset&&gainOK&&member&&beamOK&&gainTruth(first)<=c.gainMax&&norm(bEnd)<=c.priorRadius&& ...
  norm(c.sensorBias)==0&&max(abs(Z),[],'all')<=c.kappa;
end
r=struct('scenario',name,'seed',seed,'method',method,'attempted',attempted,...
 'accepted',accepted,'abstained',refused,'fit_rejected',fitRejected,'error_um',err,...
 'accepted_error_um',acceptedError,'attempt_error_um',attemptError,'radius_um',radius*1e6,...
 'coverage_all_fits',coverage,'outage_s',sum(down(eval))*c.dt,'probe_s',sum(probe)*c.dt,...
 'probe_count',double(any(probe)),'energy_urad2s',sum(angle(probe,:).^2,'all')*c.dt*1e12,...
 'tail_availability',mean(~down(tail)),'false_correction',norm(bEnd)==0 && norm(correction)>c.offsetThreshold,...
 'missed_pointing_diagnosis',norm(bEnd)>c.offsetThreshold && ~accepted,...
 'missed_diagnosis',(norm(bEnd)>0||abs(gEnd-1)>1e-10)&&~accepted,...
 'probe_induced_outage_s',probeInduced,'avoided_outage_s',avoided,...
 'diagnosis_s',diagnosis_s,'start_s',start,'finish_s',finish,'amplitude_um',selected_amplitude(plan),...
 'false_acquisition',falseAcq,'budget_violation',budgetViolation,'bound_violation',boundViolation,...
 'tube_violation',tubeViolation,'predicted_risk_s',predicted,'mode',mode,...
 'certified_probe',certified,'certificate_premises',premises,...
 'plan_runtime_s',planRuntime,'fit_runtime_s',fitRuntime,'trace_buffer_bytes',traceBytes);
r.trace=struct('t',t,'power',power,'measured_power',pm,'angle',angle,'measured_angle',qm,...
 'down',down,'probe',probe,'lower',lower,'motion',motion,'tube',tube,'command',command,...
 'plan',plan,'fit',fit,'noise_max',max(abs(Z),[],'all'),'correction',correction);
r.trace.gain_truth=gainTruth;r.trace.offset_truth=offsetTruth;r.trace.standardized_noise=Z;r.trace.state_history=stateHistory;r.trace.reference_history=referenceHistory;r.trace.terminal_state=x';
end
function y=clip(x,limit)
y=x;if norm(x)>limit,y=x*limit/norm(x);end
end
function a=selected_amplitude(p)
a=0;if ~isempty(p),a=p.amplitude*1e6;end
end
function d=decision_config(c)
% Explicit information boundary: no scenario parameters, bias, true optics or plant mismatch.
keys={'p0','alpha','alphaRange','p0Range','gainMax','kappa','delta','noise','powerNoise','dt','T',...
 'targetRadius','maxResidual','priorRadius','driftBound','serviceBudget','acquisitionBudget',...
 'detectLog','offsetThreshold','detectionCount','settleFraction','maxCorrection','sigma',...
 'maxFitIterations','fitAlpha','fitDegree','esGain','sensitivity','kfProcess','esDuration'};
d=struct;for k=1:numel(keys),d.(keys{k})=c.(keys{k});end
end
