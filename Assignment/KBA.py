import numpy as np
from data.generate_test_data import generate_test_data_df
from SmartMeter import SmartMeter
from common import create_swarms

klds = {
    "malfunctioning": [],
    "good": [],
    "stealing":[]
}

def kba(data: np.array, deviation_boundary: float, flag_boundary: float, swarm_iters: int):
    smart_meters = []
    malfunctioning = set()
    for i, record in enumerate(data):
        sm = SmartMeter(
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
            # each meter finds KLD
            # between the distribution of its own consumption
            # and the average consumption in the swarm
            meter.calc_kld_distance(deviation_boundary, klds)
            if meter.num_flags/meter.num_swarm_realisations > flag_boundary:
                flagged.add(meter)
            meter.reset()


if __name__ == "__main__":
    data = np.array(generate_test_data_df(T=200, N=50))
    # data = pd.read_csv("data/test_data_custom.csv")
    kba(data, 400, 0.1, 400)
    print(f"Min good klds: {min(klds['good'])}\n"
          f"Min stealing klds: {min(klds['stealing'])}\n"
          f"Min malfunctioning klds: {min(klds['malfunctioning'])}\n"
          f"Max good klds: {max(klds['good'])}\n"
          f"Min stealing klds: {max(klds['stealing'])}\n"
          f"Min malfunctioning klds: {max(klds['malfunctioning'])}\n"
          f"Mean good klds: {np.mean(klds['good'])}\n"
          f"Min stealing klds: {np.mean(klds['stealing'])}\n"
          f"Min malfunctioning klds: {np.mean(klds['malfunctioning'])}\n")