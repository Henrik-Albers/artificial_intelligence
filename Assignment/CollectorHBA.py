import numpy as np
from typing import List

from data.generate_test_data import generate_test_data_df
from SmartMeterHBA import SmartMeterHBA, generate_smart_meters_HBA


class CollectorHBA:
    """
    Class representing the virtual collector used for the HBA algorithm

    Args:
        smart_meters(List[SmartMeterHBA]): List of all Smart Meters in the Swarm
    """
    
    def __init__(self, data: np.ndarray, smart_meters: List[SmartMeterHBA]):
        self.smart_meters = smart_meters
        self.sm_count = len(smart_meters)
        self._data = data

    def print_collector(self):
        for sm in self.smart_meters:
            sm.print_smart_meter()
        # print(self.sm_totals)

    def calculate_totals(self, t:int):
        # DEPRECATED
        """
        DEPRECATED
        Calculates the total amount of energy used by all SMs
        of the collector for time period t.

        Args:
            t(int): Time period for which the overall consumption is calculated

        Returns:
            np.ndarray: Array of length t containing the sums of consumption  
        """

        # Data should be in array from new to old otherwise change line
        data = self._data[:, 0:t]
        totals = np.sum(data, axis=0)
        return totals


def generate_collectors(data: np.ndarray, count_collectors:int = None) -> List[CollectorHBA]:
    collector_list = []
    if count_collectors == None:
        split_index = 5
    else:
        split_index = count_collectors
    collectors_data = np.split(data, split_index)
    for collector_data in collectors_data:
        collector_list.append(
            CollectorHBA(
                data=collector_data,
                smart_meters=generate_smart_meters_HBA(collector_data)
            )
        )

    return collector_list


if __name__ == "__main__":
    data = np.array(generate_test_data_df(T=5, N=10))
    #collector = CollectorHBA(np.array(data))
    #collector.print_collector()
    #print("Collected data:")
    #collector.start_validation_process(5)

    collectors = generate_collectors(data)
    for col in collectors:
        col.print_collector()
