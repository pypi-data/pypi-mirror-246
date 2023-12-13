from fbmc_quality.linearisation_analysis.compute_functions import (
    compute_cnec_vulnerability_to_err,
    compute_linearisation_error,
    compute_linearised_flow,
)
from fbmc_quality.linearisation_analysis.dataclasses import CnecDataAndNPS, JaoDataAndNPS, PlotData
from fbmc_quality.linearisation_analysis.process_data import (
    fetch_jao_data_basecase_nps_and_observed_nps,
    load_data_for_corridor_cnec,
    load_data_for_internal_cnec,
)
