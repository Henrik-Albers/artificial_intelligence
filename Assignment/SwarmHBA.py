import numpy as np
import random
from typing import List

from CollectorHBA import CollectorHBA, generate_collectors
from data.generate_test_data import generate_test_data_df
from SmartMeterHBA import SmartMeterHBA
from VirtualCollectorHBA import VirtualCollectorHBA


class SwarmHBA:
    def __init__(self):
        self.data = np.array(generate_test_data_df(T=5, N=10))
        self.physical_collectors = generate_collectors(self.data)
        self.initialize_new_swarm(2)

    def initialize_new_swarm(self, swarm_size:int):
        sm_idxs = list(range(len(self.data)))
        rnd_sms = random.sample(sm_idxs, k=swarm_size)
        rnd_sms = [5]
        swarm_sms = []
        sm_belongs_to_col_of_index = []
        for rnd_sm in rnd_sms:
            idx_counter = 0
            for i in range(len(self.physical_collectors)):
                sms = self.physical_collectors[i].smart_meters
                len_i = len(sms)-1
                if len_i + idx_counter >= rnd_sm:
                    sm_belongs_to_col_of_index.append(i)
                    swarm_sms.append(
                        sms[rnd_sm-idx_counter]
                    )
                idx_counter += len_i
 
        count_sm_per_col = []
        for i in range(len(self.physical_collectors)):
            count_sm_per_col.append(len(self.physical_collectors[i].smart_meters))

        self.virtual_collector = VirtualCollectorHBA(
            collectors = self.physical_collectors,
            sm_sample = swarm_sms,
            count_sm_per_col = count_sm_per_col,
            sm_belongs_to_col_of_index = sm_belongs_to_col_of_index
        )

if __name__ == "__main__":
    swarm = SwarmHBA()