import math
import statistics
import numpy as np
from scipy.stats import rv_histogram


class SmartMeter:
    """
    Single Smart Meter

    Args:
        M1(np.ndarray): last t records of consumption
    """

    def __init__(self, id, readings: np.ndarray, attack_status: str) -> None:
        self.id = id
        self.attack_status = attack_status
        self.readings = np.copy(readings)
        self.salt = np.array(np.random.rand(1, len(readings))[0] * 100)
        self.swarm_size = None
        self.sum = np.copy(readings)
        self.avg_per_reading = None
        self.num_flags = 0
        self.sum_of_avg = 0
        self.avg_of_avg_readings = None

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

    def calc_flag(self, delta_boundary: float):
        own_mean = statistics.mean(self.readings)
        own_hist = rv_histogram(
            np.histogram(self.readings.astype("float64"), bins="auto", density=False), density=False
        )
        own_entropy = own_hist.entropy()

        swarm_mean = statistics.mean(self.avg_of_avg_readings)
        swarm_hist = rv_histogram(
            np.histogram(self.avg_of_avg_readings.astype("float64"), bins="auto", density=False), density=False
        )
        swarm_entropy = swarm_hist.entropy()

        delta = math.sqrt((swarm_mean - own_mean)**2 + (swarm_entropy - own_entropy)**2)
        self.num_flags += int(delta > delta_boundary)

    def calc_kld_distance(self):
        combined_data = np.concatenate((self.avg_of_avg_readings, self.readings))
        bin_edges = np.histogram_bin_edges(combined_data, bins="auto")

        swarm_hist, _ = np.histogram(self.avg_of_avg_readings, bins=bin_edges, density=True)
        own_hist, _ = np.histogram(self.readings, bins=bin_edges, density=True)

        kld = np.sum(own_hist * np.log(own_hist / swarm_hist))
        print(f"Kullback–Leibler divergence: {kld}")
