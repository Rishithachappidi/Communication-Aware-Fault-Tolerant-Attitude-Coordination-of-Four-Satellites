function [here,root]=v7_setup
here=fileparts(mfilename('fullpath'));root=fileparts(fileparts(here));addpath(fullfile(root,'research','v6'));v6_setup;addpath(here,fullfile(here,'tests'));
end
