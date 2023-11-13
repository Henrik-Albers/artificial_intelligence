import numpy as np
from typing import List

from CollectorHBA import CollectorHBA
from SmartMeterHBA import SmartMeterHBA


class VirtualCollectorHBA:
    def __init__(
        self,
        collectors: List[CollectorHBA],
        sm_sample: List[SmartMeterHBA],
        count_sm_per_col: List[int],
        sm_belongs_to_col_of_index: List[int]
    ):
        self.collectors = collectors
        self.sm_sample = sm_sample
        self.count_sm_per_col = count_sm_per_col
        self.sm_belongs_to_col_of_index = sm_belongs_to_col_of_index

    def print_vc(self):
        print(f"Count of SMs of physical collector: {self.count_sm_per_col}")
        print(f"SM belongs to physical collector: {self.sm_belongs_to_col_of_index}")

    def validate_SMs(self, t:int):
        # Get all consumption readings
        submitted_consumption = []
        for sm in self.sm_sample:
            submitted_consumption.append(sm.submit_historic_data(t=t))

        # Calculate P~
        nl = []
        for col_idx in self.sm_belongs_to_col_of_index:
            nl.append([self.collectors[col_idx].sm_count for _ in range(t)])
        nml = [[self.sm_belongs_to_col_of_index.count(x) for _ in range(t)] for x in self.sm_belongs_to_col_of_index]
        P = np.multiply(np.divide(submitted_consumption, nl), nml)

        # Start communication (also send index of sm in swarm)
        self.broadcast_ptj(P) 
        self.sm_sample[0].dist_lu_decomp(self, -1)


    def broadcast_ptj(self, P=np.ndarray):
        for idx, sm in enumerate(self.sm_sample):
            # TODO: ptj is probably not P: Probably its the sum of the values of the row
            row_sum = np.sum(P[idx, :])
            sm.update_ptj(row_sum)

    def lu_decomp_next(self, idx: int, Pt: float):
        if idx < len(self.sm_sample)-1:
            self.sm_sample[idx+1].dist_lu_decomp(self, idx+1, Pt)
