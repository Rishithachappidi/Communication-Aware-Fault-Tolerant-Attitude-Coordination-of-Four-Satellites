function start_research_v3
root=fileparts(mfilename('fullpath'));addpath(root);setup_project;
addpath(fullfile(root,'research','v3'));cd(root);
fprintf('Research V3: drift-projected optical diagnosis\n');
fprintf('Read research/v3/README.md and research/v3/paper.pdf.\n');
fprintf('test_v3              : rerun mathematical/software checks\n');
fprintf('run_v3               : new primary batch (protects existing results)\n');
fprintf('run_v3_stress        : new sensitivity batch (protects existing results)\n');
fprintf('build_v3_projection_model(4): separate estimator-only Simulink copy\n');
fprintf('To repeat a completed primary batch, use run_v3(''replication_01'').\n');
end
