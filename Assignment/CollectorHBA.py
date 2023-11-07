import numpy as np
from typing import List
from data.generate_test_data import generate_test_data_df

from SmartMeterHBA import SmartMeterHBA

def generate_smart_meters_HBA(
    data: np.ndarray
) -> List[SmartMeterHBA]:
    """
    Generates Smart Meters for the HBA algorithm

    Args:
        data(np.ndarray): historic data of the smart meter and attack status

    Returns:
        List[SmartMeterHBA]: List of SmartMetersHBAs
    """
    smart_meters = []
    for record in data:
        smart_meters.append(
                SmartMeterHBA(
                    historic_data=record[:-1],
                    attack_status=record[-1]
                )
            )
    return smart_meters


class CollectorHBA:
    """
    Class representing the virtual collector used for the HBA algorithm

    Args:
        smart_meters(List[SmartMeterHBA]): List of all Smart Meters in the Swarm
    """
    
    def __init__(self, data: np.ndarray):
        sms = generate_smart_meters_HBA(data)
        self.smart_meters = sms
        self._data = data
        # -1 to exclude the attack column
        self.sm_totals = self.calculate_totals(data.shape[1]-1)

    def print_collector(self):
        for sm in self.smart_meters:
            sm.print_smart_meter()
        print(self.sm_totals)

    def calculate_totals(self, t:int):
        """
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


    

if __name__ == "__main__":
    data = generate_test_data_df(T=5, N=10)
    collector = CollectorHBA(np.array(data))
    collector.print_collector()