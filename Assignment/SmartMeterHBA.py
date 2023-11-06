import numpy as np

class SmartMeterHBA:
    def __init__(
        self,
        historic_data: np.ndarray,
        attack_status: str
    ):
        self.historic_data = historic_data
        self.attack_status = attack_status