function [here,root]=v5_setup
here=fileparts(mfilename('fullpath'));root=fileparts(fileparts(here));
addpath(fullfile(root,'research','v4'));v4_setup;addpath(here,fullfile(here,'tests'));
end
