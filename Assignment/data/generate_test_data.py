import csv
import numpy as np
import pandas as pd
from typing import List

def generate_test_data_df(
    T,
    N,
    m_mean=10,
    attack_percentage=0.1,
    stealing_percentage=0.5,
    attack_strength=5
):
    """
    Generates  and returns dummy data for smart meters (SM)

    Args:
        T: Number of consumption records that are created for each SM 
        N: Number of SMs for which records are created for 
        m_mean: Mean of normal distribution, that is used for SM consumption generation
        attack_percentage: Percentage of how many attackers are present in dataset
        stealing_percentage: Percentage of stealing vs. malfunctioning attackers
        attack_strength: Mean of normal distribution, that is used for Attack modification

    Returns:
        DataFrame: DataFrame consisting of the generated data
    """
    data = []
    for record_idx in range(N):
        record = []
        # Attack happened
        is_attacker = np.random.choice(
            [0, 1], p=[1-attack_percentage, attack_percentage])
        # Steal or malfunction
        is_stealing = np.random.choice(
            [0, 1], p=[1-stealing_percentage, stealing_percentage])
        for t in range(T):
            value = np.random.normal(loc=m_mean)
            # Current SM is attacker
            if is_attacker == 1:
                # Current attacker is stealing or SM is malfunctioning
                modification = np.random.normal(loc=attack_strength)
                if is_stealing == 1:
                    value -= modification
                else:
                    value += modification
            record.append(value)
        # Add column with outcome
        if is_attacker == 1:
            if is_stealing == 1:
                record.append(-modification)
            else:
                record.append(modification)
        else:
            record.append(0)
        data.append(record)

    col_names = [f"t{x}" for x in range(T)]
    col_names.append("Attack")
    data_frame = pd.DataFrame(data, columns=col_names)

    return data_frame


def generate_test_data_file(
    path,
    T,
    N,
    m_mean=10,
    attack_percentage=0.1,
    stealing_percentage=0.5,
    attack_strength=5
):
    """
    Generates a csv file consisting of dummy data for smart meters (SM)

    Args:
        path: Path where the file should be created
        T: Number of consumption records that are created for each SM 
        N: Number of SMs for which records are created for 
        m_mean: Mean of normal distribution, that is used for SM consumption generation
        attack_percentage: Percentage of how many attackers are present in dataset
        stealing_percentage: Percentage of stealing vs. malfunctioning attackers
        attack_strength: Mean of normal distribution, that is used for Attack modification
    """
    data, totals = generate_test_data_df(
        T=T,
        N=N,
        m_mean=m_mean,
        attack_percentage=attack_percentage,
        stealing_percentage=stealing_percentage,
        attack_strength=attack_strength
    )
    data.to_csv(path)


if __name__ == "__main__":
    data,_ = generate_test_data_df(T=5, N=10)
    path = r"Assignment\data\test_data.csv"
    generate_test_data_file(path=path, T=5, N=10)
    print(data.head())
