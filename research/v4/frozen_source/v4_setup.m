function [here,root]=v4_setup
here=fileparts(mfilename('fullpath'));root=fileparts(fileparts(here));
addpath(root);setup_project;addpath(fullfile(root,'research','v3'),here,fullfile(here,'tests'));
end
