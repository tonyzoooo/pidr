%% SIMPLE BALL-AND-STICK MODEL
% Using this model, we intend to measure the LFPs created through simple 
% stimulation. This is to be compared to other simulation tools.
%

%% Tissue parameters
% Model of tissue, the values are approximative (extraceted from the VERTEX
% tutorials) as we don't have knowledge about this.
TissueParams.X = 2500;
TissueParams.Y = 400;
TissueParams.Z = 200;
TissueParams.neuronDensity = 50;
TissueParams.numLayers = 1;
TissueParams.layerBoundaryArr = [200, 0];
TissueParams.numStrips = 10;
TissueParams.tissueConductivity = 0.3;
TissueParams.maxZOverlap = [-1 , -1];

%% Neuron group parameters
% One kind of neuron
NeuronParams.modelProportion = 1;
NeuronParams.somaLayer = 1;

% Neuron parameters
% Here we are going to specify the neuron's traits (morphology,
% properties).

%NeuronParams.neuronModel = 'passive';
NeuronParams(1).neuronModel = 'adex';
NeuronParams(1).V_t = -50;
NeuronParams(1).delta_t = 2;
NeuronParams(1).a = 0.04;
NeuronParams(1).tau_w = 10;
NeuronParams(1).b = 40;
NeuronParams(1).v_reset = -65;
NeuronParams(1).v_cutoff = -45;
NeuronParams(1).numCompartments = 3;
NeuronParams(1).compartmentParentArr = [0, 1, 1];
NeuronParams(1).compartmentLengthArr = [25, 1000, 50];
NeuronParams(1).compartmentDiameterArr = [25, 2, 2];
NeuronParams(1).compartmentXPositionMat = ...
[   0,  25; 
    25, 1025; 
    0,  -50];
NeuronParams(1).compartmentYPositionMat = ...
[   0,  0; 
    0,  0; 
    0,  0];
NeuronParams(1).compartmentZPositionMat = ...
[   0,  0; 
    0,  0; 
    0,  0];
NeuronParams(1).axisAligned = 'y';

% Displaying the model
%viewMorphology(NeuronParams(1)); %btw there is a pb with scaling on x axis
% morphology looks fine otherwise


% neuron parameters
NeuronParams(1).C = 1;
NeuronParams(1).R_M = 6700; %résistance membrane
NeuronParams(1).R_A = 150; %résistance a
NeuronParams(1).E_leak = -65;

%% Stimulation
% Input stimulation for the LFP (somatic current) 
NeuronParams(1).Input.inputType = 'i_step';
NeuronParams(1).Input.amplitude = 0.2;%augmenter l'amplitude
NeuronParams(1).Input.timeOn = 1;
NeuronParams(1).Input.timeOff = 11;
NeuronParams(1).Input.compartmentsInput = 1;
NeuronParams(1).basalID = 3;
NeuronParams(1).apicalID = 2;

%% Connection parameters
% Synaptic connections made throughout the tissue. Speed, distribution and
% stuff.
ConnectionParams(1).numConnectionsToAllFromOne{1} = 1;
ConnectionParams(1).synapseType{1} = 'i_exp';
ConnectionParams(1).tau{1} = 2;
ConnectionParams(1).weights{1} = 0;
ConnectionParams(1).targetCompartments{1} = ...
  [NeuronParams(1).basalID, NeuronParams(1).apicalID];
ConnectionParams(1).axonArborSpatialModel = 'gaussian';
ConnectionParams(1).sliceSynapses = true;
ConnectionParams(1).axonArborRadius = 250;
ConnectionParams(1).axonArborLimit = 500;
ConnectionParams(1).axonConductionSpeed = 0.3;
ConnectionParams(1).synapseReleaseDelay = 0.5;

%% Simulation parameters

% Recording and electrodes
RecordingSettings.saveDir = '~/VERTEX_sim/';
RecordingSettings.LFP = true;
[meaX, meaY, meaZ] = meshgrid(-250:125:1250, 0, 250:-50:50);
RecordingSettings.meaXpositions = meaX;
RecordingSettings.meaYpositions = meaY;
RecordingSettings.meaZpositions = meaZ;
% RecordingSettings.minDistToElectrodeTip = 20;
% minDistToElectrodeTip – this value ensures that no neuronal compartment 
% can be positioned too close to an electrode tip and therefore 
% unrealistically dominate the LFP. We choose 20 microns, which is the 
% default value if this parameter is not set by the user.
RecordingSettings.v_m = 1;
RecordingSettings.maxRecTime = 100;
RecordingSettings.sampleRate = 1000000;


% Simulation settings
SimulationSettings.simulationTime = 8;
SimulationSettings.timeStep = 0.0001;


SimulationSettings.parallelSim = false;
SimulationSettings.poolSize = 4;
SimulationSettings.profileName = 'local';

[params, connections, electrodes] = ...
  initNetwork(TissueParams, NeuronParams, ConnectionParams, ...
              RecordingSettings, SimulationSettings);

runSimulation(params, connections, electrodes);
Results = loadResults(RecordingSettings.saveDir);
figure(2)
plot(Results.LFP(3, :), 'LineWidth', 2)
set(gcf,'color','w');
set(gca,'FontSize',16)
title('LFP at electrode 3', 'FontSize', 16)
xlabel('Time (ms)', 'FontSize', 16)
ylabel('LFP (mV)', 'FontSize', 16)


