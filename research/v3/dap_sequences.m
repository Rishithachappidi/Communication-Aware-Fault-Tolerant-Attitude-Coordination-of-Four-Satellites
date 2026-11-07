function [S,names]=dap_sequences
% Each axis has zero zeroth and first temporal moments at equal dwell.
S(:,:,1)=[1 0;-1 0;-1 0;1 0;0 1;0 -1;0 -1;0 1];
S(:,:,2)=[1 0;-1 0;0 1;0 -1;1 0;-1 0;0 1;0 -1];
names={'balanced','sequential'};
end
