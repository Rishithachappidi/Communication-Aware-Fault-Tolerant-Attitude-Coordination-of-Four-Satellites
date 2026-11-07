function v3_summarize(folder,T,examples,protocol)
rows=struct([]);rng(12345);
for a=1:numel(protocol.scenarios)
 for j=1:numel(protocol.methods)
  name=protocol.scenarios{a};method=protocol.methods{j};X=T(strcmp(T.scenario,name)&strcmp(T.method,method),:);
  row=struct('scenario',name,'method',method,'n',height(X),'accepted',sum(X.accepted),...
   'rejected',sum(X.rejected),'median_error_um',median(X.error_um,'omitnan'),...
   'mean_outage_s',mean(X.outage_s),'sd_outage_s',std(X.outage_s),...
   'mean_probe_s',mean(X.probe_s),'mean_energy_urad2s',mean(X.energy_urad2s),...
   'tail_availability',mean(X.tail_availability),'false_corrections',sum(X.false_correction),...
   'conditional_coverage',mean(X.coverage,'omitnan'));
  Y=T(strcmp(T.scenario,name)&strcmp(T.method,'constant_fit'),:);
  delta=X.outage_s-Y.outage_s;boot=mean(delta(randi(height(X),height(X),2000)),1);
  row.delta_outage_s=mean(delta);row.delta_ci_low=quantile(boot,0.025);row.delta_ci_high=quantile(boot,0.975);
  if isempty(rows),rows=row;else,rows(end+1)=row;end
 end
end
summary=struct2table(rows);writetable(summary,fullfile(folder,'summary.csv'));
% Publication plots preserve raw values and failed cases.
set(groot,'defaultFigureVisible','off','defaultAxesFontSize',12);fig=figure('Position',[50 50 1050 520]);theme(fig,'light');
tiledlayout(1,2,'Padding','compact');
nexttile;hold on;for j=[2 3 4 6]
 X=summary(strcmp(summary.method,protocol.methods{j}),:);
 plot(1:height(X),X.mean_outage_s,'-o','LineWidth',1.3,'DisplayName',strrep(protocol.methods{j},'_',' '));
end
xticks(1:numel(protocol.scenarios));xticklabels(strrep(protocol.scenarios,'_',' '));xtickangle(45);
ylabel('Mean link outage (s)');grid on;lg=legend;lg.Layout.Tile='south';lg.NumColumns=4;lg.FontSize=10;title(sprintf('(a) Service outcomes; %d paired seeds',numel(protocol.seeds)));
nexttile;hold on;for j=[2 3 4 6]
 X=summary(strcmp(summary.method,protocol.methods{j}),:);
 plot(1:height(X),X.accepted./X.n,'-o','LineWidth',1.3,'DisplayName',strrep(protocol.methods{j},'_',' '));
end
xticks(1:numel(protocol.scenarios));xticklabels(strrep(protocol.scenarios,'_',' '));xtickangle(45);
ylabel('Accepted diagnosis fraction');ylim([0 1.05]);grid on;title('(b) Rejection is an explicit outcome');
exportgraphics(fig,fullfile(folder,'comparison.pdf'),'ContentType','vector');exportgraphics(fig,fullfile(folder,'comparison.png'),'Resolution',180);close(fig);
fig=figure('Position',[50 50 1050 620]);theme(fig,'light');tiledlayout(2,2,'Padding','compact');
exampleIndices=[3 4 6 8];
for a=1:4
 name=protocol.scenarios{exampleIndices(a)};
 nexttile;hold on;for j=[2 6]
  E=examples.(name).(protocol.methods{j});plot(E.t,E.power*1e6,'LineWidth',1.2,'DisplayName',strrep(protocol.methods{j},'_',' '));
 end
 yline(protocol.config.sensitivity*1e6,'k--','Receiver sensitivity','HandleVisibility','off');
 xlabel('Time (s)');ylabel('Received power (uW)');title(strrep(name,'_',' '));grid on;legend('Location','best');
end
exportgraphics(fig,fullfile(folder,'traces.pdf'),'ContentType','vector');exportgraphics(fig,fullfile(folder,'traces.png'),'Resolution',180);close(fig);
% Machine-generated LaTeX rows: paper never contains hand-entered results.
fid=fopen(fullfile(folder,'results_rows.tex'),'w');
fprintf(fid,'%cdef%cResultRows{\n',92,92);
for a=1:numel(protocol.scenarios)
 for j=[2 3 6]
  X=summary(strcmp(summary.scenario,protocol.scenarios{a})&strcmp(summary.method,protocol.methods{j}),:);
  fprintf(fid,'%s & %s & %d/%d & %.2f & %.3f & %.3f \\\\\n',...
   strrep(X.scenario{1},'_',' '),strrep(X.method{1},'_',' '),X.accepted,X.n,...
   X.median_error_um,X.mean_outage_s,X.mean_probe_s);
 end
end
fprintf(fid,'}\n');fclose(fid);
end
