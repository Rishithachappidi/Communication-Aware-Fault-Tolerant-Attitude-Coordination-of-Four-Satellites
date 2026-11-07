function r=v3_trial(name,seed,method,c,designs)
% Closed-loop one-terminal experiment using the original repository plant.
% Common random numbers are generated once and indexed by physical time.
rng(seed,'twister');t=(0:c.dt:c.T-c.dt)';N=numel(t);Z=randn(N,5);
p=terminal_parameters(c);x=zeros(8,1);ref=zeros(2,1);q0=zeros(2,1);
power=zeros(N,1);angle=zeros(N,2);command=zeros(N,2);available=false(N,1);
probe=false(N,1);estimate=nan(N,2);label=zeros(N,1);trueB=zeros(N,2);
active=false;attempted=false;start=NaN;finish=NaN;count=0;idx=[];fit=[];
plan=struct('ok',false,'q',zeros(8,2),'dwell',0.35,'amplitude',0,'riskSeconds',NaN);
rejected=false;accepted=false;correction=zeros(2,1);fitB=[NaN;NaN];fitGain=NaN;
[S,~]=dap_sequences;
for k=1:N
 now=t(k);[b,g]=v3_truth(now,name,seed);trueB(k,:)=b';
 u=[ref;1;1;g;0;zeros(2,1);b;1];
 [~,y]=terminal_kernel(x,u,Z(k,:)',p);o=sensor_view(y);
 power(k)=y(16);angle(k,:)=y(3:4)';command(k,:)=y(11:12)';available(k)=y(18)>0;
 % Every new method has the same observable residual trigger and gets one attempt.
 nominal=c.p0*exp(-2*sum(o.angle.^2)/c.alpha^2);
 anomaly=abs(log(max(o.power,0.0001*c.p0)/max(nominal,0.0001*c.p0)))>c.detectLog;
 if now>1 && anomaly,count=count+1;else,count=0;end
 if count>=c.detectionCount && ~attempted && ~strcmp(method,'passive')
  attempted=true;q0=o.angle;
  if o.power<=0.005*c.p0
   plan.ok=false;
  elseif strcmp(method,'DAP') || strcmp(method,'no_service')
   plan=dap_plan(o.power,c,designs,strcmp(method,'DAP'));
  else
   plan.ok=true;plan.q=6e-6*S(:,:,2);plan.dwell=0.35;plan.amplitude=6e-6;
   if strcmp(method,'balanced_fixed'),plan.q=6e-6*S(:,:,1);end
  end
  if plan.ok,active=true;start=now;else,rejected=true;end
 end
 if active
  age=now-start;phase=min(8,floor((age+1e-9)/plan.dwell)+1);
  if age<8*plan.dwell-1e-9
   ref=plan.q(phase,:)';probe(k)=true;
   if mod(age+1e-9,plan.dwell)>=c.settleFraction*plan.dwell,idx(end+1)=k;end
  else
   active=false;finish=now;ref=zeros(2,1);
   degree=1;if strcmp(method,'constant_fit'),degree=0;end
   % Public sensors only; use encoder angle, never the hidden plant angle.
   fit=dap_fit(t(idx),angle(idx,:)+c.noise*Z(idx,1:2),...
     max(0,power(idx).*(1+c.powerNoise*Z(idx,5))),c,degree);
   fitB=fit.b;fitGain=fit.gain;accepted=fit.ok;
   if any(strcmp(fit.reason,{'censored','rank','temporal-rank','insufficient-data'})),fitB=[NaN;NaN];end
   if fit.ok && norm(fit.b)>c.offsetThreshold && c.p0*fit.gain>1.05*c.sensitivity
    correction=-fit.b;
    if norm(correction)>c.maxCorrection,correction=correction*c.maxCorrection/norm(correction);end
   end
   ref=correction;
  end
 end
 if accepted
  estimate(k,:)=fitB';
  label(k)=double(norm(fitB)>c.offsetThreshold)+2*double(fitGain<0.8);
 elseif attempted,label(k)=4;end
 x=v3_advance(x,u,Z(k,:)',p,c.dt);
end
eval=t>=2;tail=t>=max(2,c.T-2);[bEnd,~]=v3_truth(c.T-c.dt,name,seed);
error=NaN;if all(isfinite(fitB)),error=norm(fitB-bEnd)*1e6;end
coverage=NaN;if accepted,coverage=double(norm(fitB-bEnd)<=fit.radius);end
r=struct('scenario',name,'seed',seed,'method',method,'attempted',attempted,...
 'rejected',rejected,'accepted',accepted,'error_um',error,'coverage',coverage,...
 'outage_s',sum(~available(eval))*c.dt,'probe_s',sum(probe)*c.dt,...
 'energy_urad2s',sum(angle(probe,:).^2,'all')*c.dt*1e12,...
 'tail_availability',mean(available(tail)),'false_correction',...
 norm(bEnd)==0 && norm(correction)>c.offsetThreshold,'amplitude_um',plan.amplitude*1e6,...
 'start_s',start,'finish_s',finish,'predicted_risk_s',plan.riskSeconds);
r.trace=struct('t',t,'power',power,'angle',angle,'command',command,'probe',probe,...
 'available',available,'estimate',estimate,'label',label,'truth_b',trueB,'plan',plan,'fit',fit);
end
