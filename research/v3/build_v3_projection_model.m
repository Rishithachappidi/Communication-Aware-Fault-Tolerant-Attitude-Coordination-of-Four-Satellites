function name=build_v3_projection_model(n)
% Creates a separate opt-in Simulink model. Original V2 files stay untouched.
% This checks estimator integration, not the complete new DAP planner.
if nargin<1,n=4;end
here=fileparts(mfilename('fullpath'));root=fileparts(fileparts(here));
addpath(root);setup_project;addpath(fullfile(root,'revisions','v2'));setup_v2;addpath(here);
generated=fullfile(here,'generated');if ~isfolder(generated),mkdir(generated);end
source=fileread(fullfile(root,'revisions','v2','supervisor_v2.m'));
source=strrep(source,'supervisor_v2','supervisor_v3_projection');
source=strrep(source,'v2_decision_step','v3_projection_decision_step');
write_source(fullfile(generated,'supervisor_v3_projection.m'),source);
source=fileread(fullfile(root,'revisions','v2','v2_decision_step.m'));
source=strrep(source,'v2_decision_step','v3_projection_decision_step');
source=strrep(source,'v2_optical_fit','v3_optical_fit');
write_source(fullfile(generated,'v3_projection_decision_step.m'),source);addpath(generated);
old=sprintf('SatelliteOpticalNetwork_%d_v2',n);name=sprintf('SatelliteOpticalNetwork_%d_projection_v3',n);
target=fullfile(generated,[name '.slx']);
if ~isfile(target)
 load_system(fullfile(root,'revisions','v2','models',[old '.slx']));
 save_system(old,target);close_system(old,0);
 load_system(target);set_param([name '/Supervisor'],'FunctionName','supervisor_v3_projection');save_system(name);
else,load_system(target);end
end
function write_source(path,source)
fid=fopen(path,'w');assert(fid>=0);fprintf(fid,'%s',source);fclose(fid);
end
