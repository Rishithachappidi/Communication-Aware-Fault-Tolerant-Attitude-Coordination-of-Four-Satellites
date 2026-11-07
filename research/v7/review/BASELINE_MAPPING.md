# Baseline fidelity and resource mapping

All numerical extension comparisons use the inherited V6 causal trigger and terminal, six unchanged settings, paired seeds7001–7100, six finite actual actuator pairs and maximum2.88s excitation. Source is frozen before new outcomes. This extension was frozen after original selector outcomes; it is exploratory, not an untouched four-method confirmation.

|Candidate|Implemented here|Actual fidelity / remaining work|
|---|---|---|
|Fixed 2μrad guard|Preserved V6 records,7200original two-method runs|Same gate, information test, library constraint validity and ranking. Fixed delivered-motion margin is a heuristic, not a proven enclosure.|
|Parameter Kalman filter|3600new runs|Four-state linear parameter filter on transformed optics; Joseph covariance; inherited Q=0; fixed6μrad eight-dwell waveform. Approximate measurement variance/EIV treatment. Standard architecture, not full stochastic constrained-AFD.|
|Conventional ES|3600new runs|4μrad dither,0.25/0.4Hz, washout/demodulation/filter/integral adaptation gain.3. Same2.88s cap, less than slow-dither period. No diagnostic-fit output. Not safety-filtered ES.|
|Guo et al. chance-AFD|Not faithfully reproduced|Need optical nonlinear-to-stochastic-model mapping, hypotheses, informative objective and matching constraints; generic KF is not this method.|
|Massa–Paulson guaranteed AFD|Not faithfully reproduced|Author code https://github.com/PaulsonLab/Guaranteed_AFD_ADL; preserved checked active MATLAB path lacks CORA reach/interval, YALMIP sdpvar and Gurobi (`research/v5/results/verification/actuator.json`). Need dependency installation, optical mapping and verification; no surrogate result attributed to author code.|
|Williams et al. safety-filtered ES|Not faithfully reproduced|Unknown-barrier safety filter, its tuning and proof hypotheses have not been mapped to the measured optical terminal; conventional ES does not inherit that guarantee.|
|Yan optical margin-aware scanning|No faithful reproduction|Different acquisition scan objective; complete optical mapping and original implementation unresolved.|
|Oh–Noh correlated-retry acquisition|No faithful reproduction|Publisher abstract/metadata only; full text not accessible in this session. Exact overlap not excluded.|

Equal time and common plant constraints do not imply equal realized angular energy. The parameter filter's larger waveform and no authorization refusal are disclosed. Its600accepted fits versus594for UAD at R1middle are retained; zero outage for both prevents a claim of empirical service superiority. Accepted-fit confidence misses15versus26 use different approximate covariances and selected populations, not a proof of comparative calibration.

The raw baseline functions are inherited `research/v4/parameter_kf_fit.m` and the ES branch of `research/v6/v6_trial.m`. Prior development tuning used seeds41–45; new outcome seeds7001–7100. No new tuning was chosen after extension outcomes.
