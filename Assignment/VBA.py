import numpy as np

from data.generate_test_data import generate_test_data_df
from SmartMeter import SmartMeter


class VBA:
    def __init__(self):
        data = generate_test_data_df(T=5, N=10)
        data = np.array(data)
        smart_meters = []
        for record in data:
            smart_meters.append(
                SmartMeter(
                    M1=record[:-1],
                    attack_status=record[-1]
                )
            )
        self.smart_meters = smart_meters


if __name__ == "__main__":
    vba = VBA()
    print(vba.smart_meters[0].M1)
    print(vba.smart_meters[0].own_entropy)
