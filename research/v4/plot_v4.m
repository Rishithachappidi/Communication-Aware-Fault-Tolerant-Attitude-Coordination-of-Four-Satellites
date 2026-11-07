function plot_v4(tag)
if nargin<1,tag='final';end
[here,~]=v4_setup;folder=fullfile(here,'results',tag);
T=readtable(fullfile(folder,'primary_summary.csv'));S=readtable(fullfile(folder,'sensitivity_summary.csv'));
load(fullfile(folder,'protocol.mat'),'P');set(groot,'defaultFigureVisible','off','defaultAxesFontSize',14);
methods={'projected_fixed','DAP','projected_noise','parameter_kf','lockin','UAD'};
names={'Fixed projection','DAP','Noise-aware fixed','Parameter KF','Lock-in ES','UAD'};
f=figure('Position',[30 30 1150 500]);theme(f,'light');tiledlayout(1,2,'Padding','compact');
nexttile;Y=zeros(9,numel(methods));
for i=1:9,for j=1:numel(methods),r=T(strcmp(T.scenario,P.scenarios{i})&strcmp(T.method,methods{j}),:);Y(i,j)=r.mean_outage_s;end,end
bar(Y);ylabel('Mean outage (s)');ylim([0 13]);grid on;title('(a) Primary service outcomes');
xticks(1:9);labels={'Healthy','Pointing','Affine drift','Gain only','Quadratic','Fast gain','Deep loss','Near threshold','Dark'};
xticklabels(labels);xtickangle(45);lg=legend(names,'NumColumns',3,'FontSize',14);lg.Layout.Tile='south';
nexttile;Y=zeros(9,4);
for i=1:9
 r=T(strcmp(T.scenario,P.scenarios{i})&strcmp(T.method,'UAD'),:);
 Y(i,:)=[r.accepted r.fit_rejected r.abstained r.n-r.attempted]/r.n;
end
bar(Y,'stacked');ylabel('Run fraction');ylim([0 1.05]);grid on;title('(b) UAD diagnosis coverage');
xticks(1:9);xticklabels(labels);xtickangle(45);
legend({'Accepted','Fit rejected','Abstained','No trigger'},'Location','northoutside','NumColumns',2,'FontSize',13);
emit(f,folder,'primary_comparison');

f=figure('Position',[30 30 1100 760]);theme(f,'light');tiledlayout(2,2,'Padding','compact');
styles={'-o','-s','-d','-^','-x'};ms={'DAP','projected_noise','parameter_kf','lockin','UAD'};
labs={'DAP','Noise-aware fixed','Parameter KF','Lock-in ES','UAD'};
for panel=1:4
 nexttile;hold on;
 for j=1:numel(ms)
  if panel<4
   r=S(strcmp(S.condition,'noise')&strcmp(S.method,ms{j}),:);
   scenario='linear_drift';if panel==3,scenario='near_threshold';end
   r=r(strcmp(r.scenario,scenario),:);[x,order]=sort(r.condition_value);r=r(order,:);
  else
   r=S(strcmp(S.condition,'bias')&strcmp(S.method,ms{j})&strcmp(S.scenario,'linear_drift'),:);
   [x,order]=sort(r.condition_value);r=r(order,:);
  end
  switch panel
   case 1,y=r.mean_outage_s;
   case 2,y=r.accepted./r.n;if strcmp(ms{j},'lockin'),y(:)=NaN;end
   case 3,y=r.mean_probe_induced_outage_s;
   case 4,y=r.coverage_accepted;
  end
  plot(x,y,styles{j},'LineWidth',1.4,'MarkerSize',6,'DisplayName',labs{j});
 end
 grid on;
 switch panel
  case 1,title('(a) Affine drift');ylabel('Mean outage (s)');xlabel('Noise multiplier');
  case 2,title('(b) Diagnosis coverage');ylabel('Accepted fraction');xlabel('Noise multiplier');ylim([0 1.05]);
  case 3,title('(c) Near-threshold service');ylabel('Probe-induced outage (s)');xlabel('Noise multiplier');
  case 4,title('(d) Unmodeled encoder bias');ylabel('Coverage among accepted fits');xlabel('Bias amplitude (urad)');ylim([0 1.05]);
 end
 if panel==1,lg=legend('NumColumns',3,'FontSize',14);lg.Layout.Tile='south';end
end
emit(f,folder,'sensitivity');

x=load(fullfile(folder,'primary_linear_drift.mat'),'traces');j=find(strcmp(P.methods,'UAD'));z=x.traces{1,j};
f=figure('Position',[30 30 1100 430]);theme(f,'light');tiledlayout(1,2,'Padding','compact');
nexttile;semilogy(z.t,max(z.power*1e6,1e-6),'LineWidth',1.3,'DisplayName','Actual power');hold on;
semilogy(z.t,z.lower*1e6,'--','LineWidth',1.6,'DisplayName','Conditional lower bound');
yline(P.config.sensitivity*1e6,'k:','Sensitivity','HandleVisibility','off');
xlabel('Time (s)');ylabel('Power (uW), log scale');title('(a) Seed 3001: affine drift');grid on;legend('Location','best','FontSize',14);
nexttile;mask=isfinite(z.tube);first=find(z.probe,1);q0=z.angle(first,:);
err=vecnorm(z.angle(mask,:)-q0-z.motion(mask,:),2,2)*1e6;
plot(z.t(mask),err,'LineWidth',1.3,'DisplayName','Delivered-increment error');hold on;
plot(z.t(mask),z.tube(mask)*1e6,'--','LineWidth',1.6,'DisplayName','Declared tube radius');
xlabel('Time (s)');ylabel('Angle (urad)');title('(b) Sampled tube containment');grid on;legend('Location','best','FontSize',14);
emit(f,folder,'certificate_trace');
end
function emit(f,folder,name)
exportgraphics(f,fullfile(folder,[name '.pdf']),'ContentType','vector');
exportgraphics(f,fullfile(folder,[name '.png']),'Resolution',170);close(f);
end
