import numpy as np
from data.generate_test_data import generate_test_data_df
from SmartMeter import SmartMeter
from common import create_swarms


def vba(data: np.array, deviation_boundary: float, flag_boundary: int, swarm_iters: int):
    smart_meters = []
    malfunctioning = set()
    for i, record in enumerate(data):
        sm = SmartMeter(
                id=i,
                readings=record[1:-2],
                attack_status=record[-1]
            )
        smart_meters.append(sm)
        if record[-1] == "malfunctioning":
            malfunctioning.add(sm)

    swarms = create_swarms(smart_meters, swarm_iters)
    flagged = set()
    for swarm in swarms:
        num_smart_meters = len(swarm)

        for i, meter in enumerate(swarm):
            # reset variables for current meter
            meter.set_swarm_size(num_smart_meters)
            meter.encrypt_sum()
            # add up all the readings for current meter
            for j in range(num_smart_meters):
                sender_index = (i + j) % num_smart_meters
                receiver_index = (i + j + 1) % num_smart_meters
                swarm[sender_index].send_sum(swarm[receiver_index])
            # calculate current meter's avg
            meter.calc_avg()

        for i, meter in enumerate(swarm):
            # share the average with the swarm
            meter.encrypt_avg_sum()
            for j in range(num_smart_meters):
                sender_index = (i + j) % num_smart_meters
                receiver_index = (i + j + 1) % num_smart_meters
                swarm[sender_index].send_avg(swarm[receiver_index])
            meter.calc_avg_avg()

        for meter in swarm:
            meter.calc_flag(deviation_boundary)
            if meter.num_flags > flag_boundary:
                flagged.add(meter)
            meter.reset()

    if malfunctioning == flagged:
        print("All smart meters marked correctly")
    else:
        for f in flagged:
            if f.attack_status != 'malfunctioning':
                print("U done goofed")


if __name__ == "__main__":
    data = np.array(generate_test_data_df(T=5, N=500))
    # data = pd.read_csv("data/test_data_custom.csv")
    vba(data, 3, 50, 10)


