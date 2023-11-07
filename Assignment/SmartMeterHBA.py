import numpy as np

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
    