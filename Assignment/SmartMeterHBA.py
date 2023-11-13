import numpy as np
from typing import List

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from VirtualCollectorHBA import VirtualCollectorHBA

class SmartMeterHBA:
    def __init__(
        self,
        historic_data: np.ndarray,
        attack_status: str
    ):
        # value incl. attack
        self._historic_data = historic_data
        self._attack_status = attack_status
        # real value of SM without attack
        self._historic_data_true = np.subtract(historic_data, attack_status)

    def print_smart_meter(self):
        print("##### SM #####")
        print(f"Combined: {self._historic_data}")
        print(f"Attack: {self._attack_status}")
        print(f"True value: {self._historic_data_true}")

    def submit_historic_data(self, t:int):
        """
        Method used by the collector to retrieve consumption data of period t

        Args:
            t(int): t is the time span for which the consumption readings are requested

        Returns:
            np.ndarray: last t consumption readings for the SM
        """
        return self._historic_data[:t]
    
    def update_ptj(self, ptj:np.ndarray):
        self.ptj = ptj

    def dist_lu_decomp(self, v_col: "VirtualCollectorHBA", j: int, Pt=None, previous_l: np.ndarray = None, previous_u: np.ndarray = None):
        if j == -1:
            # SM is first SM of virtual collector
            # TODO: No it is the collectors SM of LU paper
            Pt = self.ptj
            v_col.lu_decomp_next(j, Pt)
        else:
            v_col_len = len(v_col.sm_sample)
            if j < v_col_len:
                # compute u
                # for q in range(1, j):
                u = self.compute_u(j, previous_l, v_col_len)
                print(u)
                # compute l

                # compute y

                # transmit data and notify next
                v_col.lu_decomp_next(j, Pt, previous_u=u)
            else:
                # SM is last SM of virtual collector
                pass

    def compute_u(self, j:int, previous_l: np.ndarray, previous_u: np.ndarray, v_col_len: int):
        # TODO: Complain about privacy concerns. Normal LU uses SM0 (Collector) to mask consumption of SM1.
        #       The new algorithm lets SM1 send the data plainly to SM2
        if j == 0:
            return self._historic_data
        hist_data = self._historic_data
        first_elem = hist_data[0]
        u = []
        for i in range(0, v_col_len):
            u.append(first_elem - previous_l[i,j-1] * previous_u[i-1,j])
        return np.array(u)

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
    