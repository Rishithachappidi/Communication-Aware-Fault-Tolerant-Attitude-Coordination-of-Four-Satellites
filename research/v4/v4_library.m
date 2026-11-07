function lib=v4_library(c)
% Conditional finite-model reachability tube. No continuous parameter-set claim.
[S,~]=dap_sequences;lib=struct([]);N=ceil(c.T/c.dt);
noiseBox=c.kappa*[c.noise;2*c.noise];
[An,Bn]=pid_discrete(c,1,1);
for dwell=c.dwells
 for amplitude=c.amplitudes
  t=(0:c.dt:8*dwell-c.dt)';q=amplitude*S(:,:,1);
  ref=q(min(8,floor((t+1e-9)/dwell)+1),:);meanN=zeros(4,2);motion=zeros(numel(t),2);
  for i=1:numel(t),motion(i,:)=meanN(1,:);meanN=An*meanN+Bn(:,1)*ref(i,:);end
  radius=zeros(numel(t),1);tubeValid=true;
  for jf=c.Jfactors
   for tf=c.taufactors
    [Ad,Bd,A,B]=pid_discrete(c,jf,tf);
    % Marginal state bounds from exact finite impulse responses, not |A|^N wrapping.
    H=Bd(:,2:3);stateRad=zeros(4,1);
    for k=1:N,stateRad=stateRad+abs(H)*noiseBox;H=Ad*H;end
    meanP=zeros(4,2);Cs=[-c.J*c.kp c.b-c.J*c.kd 0 -c.J*c.ki];
    stageH=zeros(4,4,4);stageJ=zeros(4,3,4);stageH(:,:,1)=eye(4);
    rawNoise=zeros(4,1);rateNoise=zeros(4,1);
    for stage=2:4
     factor=c.dt/2;if stage==4,factor=c.dt;end
     stageH(:,:,stage)=eye(4)+factor*A*stageH(:,:,stage-1);
     stageJ(:,:,stage)=factor*(A*stageJ(:,:,stage-1)+B);
    end
    for stage=1:4
     Hnoise=Bd(:,2:3);Craw=Cs*stageH(:,:,stage);Crate=stageH(2,:,stage);
     for k=1:N
      rawNoise(stage)=rawNoise(stage)+abs(Craw*Hnoise)*noiseBox;
      rateNoise(stage)=rateNoise(stage)+abs(Crate*Hnoise)*noiseBox;Hnoise=Ad*Hnoise;
     end
     rawNoise(stage)=rawNoise(stage)+abs(Cs*stageJ(:,2:3,stage)+[-c.J*c.kp c.b-c.J*c.kd])*noiseBox;
     rateNoise(stage)=rateNoise(stage)+abs(stageJ(2,2:3,stage))*noiseBox;
    end
    for i=1:numel(t)
     % Ball enclosing each model's angle and all bounded held sensor disturbances.
     radius(i)=max(radius(i),norm(meanP(1,:)-motion(i,:))+sqrt(2)*stateRad(1));
     % Check RK4 stage constraint containment. If any clamp might activate, reject certificate.
     for stage=1:4
      stageMean=stageH(:,:,stage)*meanP+stageJ(:,1,stage)*ref(i,:);
      raw=Cs*stageMean+c.J*c.kp*ref(i,:);
      tubeValid=tubeValid && all(abs(raw)+rawNoise(stage)<c.umax) && ...
       all(abs(stageMean(2,:))+rateNoise(stage)<c.rateMax);
     end
     meanP=Ad*meanP+Bd(:,1)*ref(i,:);
    end
   end
  end
  keep=mod(t+1e-9,dwell)>=c.settleFraction*dwell;
  tt=t(keep)-mean(t(keep));V=[ones(sum(keep),1) tt];Q=motion(keep,:)/c.alpha;
  [U,~]=qr(V,0);F=(Q-U*(U'*Q))'*(Q-U*(U'*Q));
  % Approximate statistical design radius includes angle-error sensitivity at the prior boundary.
  sigma=sqrt(c.powerNoise^2+(4*c.noise*(c.priorRadius+max(vecnorm(motion,2,2)))/c.alpha^2)^2);
  radius95=c.alpha*sigma/4*sqrt(5.991464547/max(min(eig(F)),eps));
  d=struct('q',q,'dwell',dwell,'amplitude',amplitude,'time',t,'motion',motion,...
   'tube',radius,'valid',tubeValid,'duration',8*dwell,'radius',radius95,'F',F);
  if isempty(lib),lib=d;else,lib(end+1)=d;end
 end
end
lib=lib(1:min(numel(lib),c.libraryLimit));
end
