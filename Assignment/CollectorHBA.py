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
        sm_totals(List[int]): List of sum of consumptions of all SMs for time t
    """
    
    def __init__(self, smart_meters: List[SmartMeterHBA], sm_totals: List[int]):
        self.smart_meters = smart_meters
        self.sm_totals = sm_totals

    def print_collector(self):
        for sm in self.smart_meters:
            print(sm.historic_data)
        print(self.sm_totals)

    

if __name__ == "__main__":
    data, totals = generate_test_data_df(T=5, N=10)
    sms = generate_smart_meters_HBA(np.array(data))
    collector = CollectorHBA(sms, totals)
    collector.print_collector()