import math
import statistics
import numpy as np


class SmartMeter:
    """
    Single Smart Meter

    Args:
        M1(np.ndarray): last t records of consumption
    """

    def __init__(self, readings: np.ndarray, attack_status: str) -> None:
        self.attack_status = attack_status
        self.readings = np.copy(readings)
        self.salt = np.array(np.random.rand(1, len(readings))[0] * 100)
        self.swarm_size = None
        self.sum = np.copy(readings)
        self.avg_per_reading = None
        self.num_flags = 0
        self.num_swarm_realisations = 0
        self.sum_of_avg = 0
        self.avg_of_avg_readings = None

    def increment_swarm_count(self):
        self.num_swarm_realisations += 1

    def reset(self):
        self.swarm_size = None
        self.sum = np.copy(self.readings)
        self.avg_per_reading = None
        self.sum_of_avg = 0
        self.avg_of_avg_readings = None

    def set_swarm_size(self, swarm_size: int):
        self.swarm_size = swarm_size

    def __decrypt_sum(self):
        self.sum -= (self.salt + self.readings)

    def encrypt_sum(self):
        self.sum += self.salt

    def __decrypt_avg_sum(self):
        self.sum_of_avg -= self.salt

    def encrypt_avg_sum(self):
        self.sum_of_avg += self.salt

    def __receive_sum(self, previous_sum: np.ndarray):
        self.sum += previous_sum

    def __receive_avg(self, previous_sum: np.ndarray):
        self.sum_of_avg += previous_sum

    def send_sum(self, next_meter):
        next_meter.__receive_sum(self.sum)
        self.sum = np.copy(self.readings)

    def send_avg(self, next_meter):
        next_meter.__receive_avg(self.sum_of_avg)
        self.sum_of_avg = 0

    def calc_avg(self):
        self.__decrypt_sum()
        self.avg_per_reading = self.sum / self.swarm_size
        self.sum = np.copy(self.readings)
        self.sum_of_avg = self.avg_per_reading

    def calc_avg_avg(self):
        self.__decrypt_avg_sum()
        self.avg_of_avg_readings = self.sum_of_avg / self.swarm_size

    def calc_flag(self, delta_boundary: float, deltas: dict):
        combined_data = np.concatenate((self.avg_of_avg_readings, self.readings))
        bin_edges = np.histogram_bin_edges(combined_data, bins="auto")

        own_mean = statistics.mean(self.readings)
        own_hist, _ = np.histogram(self.readings, bins=bin_edges, density=True)

        swarm_mean = statistics.mean(self.avg_of_avg_readings)
        swarm_hist, _ = np.histogram(self.avg_of_avg_readings, bins=bin_edges, density=True)

        bin_width = np.diff(bin_edges)

        own_hist[own_hist == 0] = 0.001
        swarm_hist[swarm_hist == 0] = 0.001

        pdf_swarm = swarm_hist * bin_width
        pdf_own = own_hist * bin_width

        own_entropy = -np.sum(pdf_own * np.log(pdf_own.astype("float64")))
        swarm_entropy = -np.sum(pdf_swarm * np.log(pdf_swarm.astype("float64")))

        delta = math.sqrt((swarm_mean - own_mean)**2 + (swarm_entropy - own_entropy)**2)
        if self.attack_status == "malfunctioning":
            deltas["malfunctioning"].append(delta)
        else:
            if self.attack_status == "stealing":
                deltas["stealing"].append(delta)
            else:
                deltas["good"].append(delta)
        self.num_flags += int(delta > delta_boundary)

    def calc_kld_distance(self, delta_boundary: float, klds: dict):
        combined_data = np.concatenate((self.avg_of_avg_readings, self.readings))
        bin_edges = np.histogram_bin_edges(combined_data, bins="auto")

        swarm_hist, swarm_bins = np.histogram(self.avg_of_avg_readings, bins=bin_edges, density=True)
        own_hist, own_bins = np.histogram(self.readings, bins=bin_edges, density=True)

        # Bin width
        bin_width = np.diff(swarm_bins)
        
        # Normalization
        pdf_swarm = swarm_hist * bin_width
        pdf_own = own_hist * bin_width

        pdf_own[pdf_own == 0] = 0.001
        pdf_swarm[pdf_swarm == 0] = 0.001

        kld = np.sum(pdf_own * np.log((pdf_own / pdf_swarm).astype('float64')))

        if self.attack_status == "malfunctioning":
            klds["malfunctioning"].append(kld)
        else:
            if self.attack_status == "stealing":
                klds["stealing"].append(kld)
            else:
                klds["good"].append(kld)
        self.num_flags += int(kld > delta_boundary)
