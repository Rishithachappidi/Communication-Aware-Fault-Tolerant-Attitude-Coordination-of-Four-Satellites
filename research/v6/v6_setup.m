function [here,root]=v6_setup
here=fileparts(mfilename('fullpath'));root=fileparts(fileparts(here));addpath(fullfile(root,'research','v5'));v5_setup;addpath(here,fullfile(here,'tests'));
end
