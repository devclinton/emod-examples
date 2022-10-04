import os

import pandas as pd

from idmtools.analysis.analyze_manager import AnalyzeManager
from idmtools.core import ItemType
from idmtools.core.platform_factory import Platform
from idmtools.entities.ianalyzer import IAnalyzer
from idmtools.entities.simulation import Simulation


class PfPRAnalyzer(IAnalyzer):

    def __init__(self, sweep_variables=None, working_dir="."):
        super(PfPRAnalyzer, self).__init__(working_dir=working_dir,
                                           filenames=["output/MalariaSummaryReport_AnnualAverage.json"])

        self.sweep_variables = sweep_variables or ["Run_Number"]

    def map(self, data, simulation: Simulation):
        # column = "initial_prev" if simulation.experiment.exp_name == "initial" else "final_prev"
        age_bins = data[self.filenames[0]]["Metadata"]["Age Bins"]
        channeldata = data[self.filenames[0]]["DataByTimeAndAgeBins"]["Average Population by Age Bin"]
        simdata = pd.DataFrame(channeldata).transpose()
        # add headers for each column as AveragePopulationByAgeBinByDate_{date}
        columns = [f'AveragePopulationByAgeBinByDate_{i}' for i in
                   data[self.filenames[0]]['DataByTime']['Time Of Report']]
        simdata.columns = columns

        simdata["age"] = age_bins

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                simdata[sweep_var] = simulation.tags[sweep_var]
            else:
                simdata[sweep_var] = 0
        return simdata

    def reduce(self, all_data):
        data_sets_per_experiment = {}

        for simulation, associated_data in all_data.items():
            experiment_name = simulation.experiment.name if simulation.experiment.name is not None else simulation.name
            if experiment_name not in data_sets_per_experiment:
                data_sets_per_experiment[experiment_name] = []

            data_sets_per_experiment[experiment_name].append(associated_data)

        os.makedirs(self.working_dir, exist_ok=True)
        for experiment_name, data_sets in data_sets_per_experiment.items():
            d = pd.concat(data_sets).reset_index(drop=True)
            d.to_csv(os.path.join(self.working_dir, f"{experiment_name}.csv"), index=False)


if __name__ == "__main__":
    # platform = Platform("Calculon")
    platform = Platform("Belegost")
    out_dir = os.path.join(os.path.expanduser('~'), 'Dropbox (IDM)', 'Malaria Team Folder', 'projects',
                           'map_intervention_impact', 'lookup_tables')

    out_dir = "output"
    run_type = "exp"
    if run_type == "exp":
        exp_ids = []
        experiments = ["6a7ca1e1-86fc-eb11-a9ed-b88303911bc1"]  # TODO, change to new experiment id in Calculon
        for exp_id in experiments:
            exp_ids.append((exp_id, ItemType.EXPERIMENT))

    elif run_type == "suite":
        exps = platform.get_children("697ca1e1-86fc-eb11-a9ed-b88303911bc1", ItemType.SUITE)
        exp_ids = []
        for exp in exps:
            exp_ids.append((exp.id, ItemType.EXPERIMENT))

    am = AnalyzeManager(ids=exp_ids, analyzers=[PfPRAnalyzer(working_dir=out_dir,
                                                             sweep_variables=["Site_Name",
                                                                              "Run_Number",
                                                                              "x_Temporary_Larval_Habitat",
                                                                              "ACT_Coverage",
                                                                              "IRS_Coverage",
                                                                              "ITN_Coverage"
                                                                              ])], partial_analyze_ok=True)
    am.analyze()