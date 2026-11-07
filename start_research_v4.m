function start_research_v4
root=fileparts(mfilename('fullpath'));addpath(root,fullfile(root,'research','v4'));v4_setup;cd(root);
fprintf('Optical research V4: reference-relative conditional service certificate\n');
fprintf('Guide: research/v4/README.md\nPaper: research/v4/paper.pdf\n');
fprintf('test_v4                  : mathematical/model regression tests\n');
fprintf('run_v4(''replication_01'') : full new experiment folder, preserving final data\n');
fprintf('plot_v4                  : regenerate supplied final figures\n');
fprintf('All original V3 files are preserved. Read the audit and limitations before using results.\n');
end
