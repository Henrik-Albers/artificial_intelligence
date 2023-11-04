import math
import numpy as np
import random
from typing import List
import statistics


class SmartMeter:
    """
    Single Smart Meter

    Args:
        M1(List[int]): last t records of consumption
    """

    def __init__(self, M1: List[int]) -> None:
        self.M1 = M1
        self.T = len(M1)
        self.Y = random.sample(range(100), self.T)
        self.own_mean = statistics.mean(M1)
        self.own_proba_hist = self.calculate_proba_hist(M1)
        self.own_entropy = self.calculate_entropy(M1)

    def calculate_proba_hist(self, elems: List[int]):
        """
        Calculates probability distribution from given histogram

        Args:
            elems(List[int]): Elements over which the probability is calculated

        Returns:
            List[int]: Returns a list containing the probabilities of each element
        """
        probabilities = [elems.count(x)/len(elems) for x in elems]
        return probabilities

    def calculate_entropy(self, elems: List[int]):
        """
        Calculates entropy based on the formula given in the paper

        Args:
            elems(List[int]): Elements over which the entropy is calculated

        Returns:
            int: Entropy of the given list
        """
        entropy = 0
        for elem in elems:
            entropy += elem*math.log(elem)
        entropy = -entropy
        return entropy


if __name__ == "__main__":
    sm = SmartMeter(M1=[1, 2, 2, 3])
    sm2 = SmartMeter(M1=[1, 2, 3, 4])
    print(sm.own_proba_hist)
    print(sm.own_entropy)
    print(sm2.own_entropy)
