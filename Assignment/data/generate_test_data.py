import numpy as np
import pandas as pd


def generate_test_data_df(
    T,
    N,
    m_mean=1000,
    attack_percentage=0.1,
    attack_strength=800
):
    """
    Generates  and returns dummy data for smart meters (SM)

    Args:
        T: Number of consumption records that are created for each SM 
        N: Number of SMs for which records are created for 
        m_mean: Mean of normal distribution, that is used for SM consumption generation
        attack_percentage: Percentage of how many attackers are present in dataset
        attack_strength: Mean of normal distribution, that is used for Attack modification

    Returns:
        DataFrame: DataFrame consisting of the generated data
    """
    data = []
    for record_idx in range(int(N - attack_percentage * N)):
        record = []
        for t in range(T):
            value = np.random.normal(loc=m_mean, scale=3)
            record.append(value)
        record.append("ok")
        data.append(record)

    for record_idx in range(int(attack_percentage * N)):
        record = []
        for t in range(T):
            value = np.random.normal(loc=m_mean, scale=3)
            modification = np.random.normal(loc=attack_strength)
            value -= modification
            record.append(value)
        record.append("stealing")
        data.append(record)

    col_names = [f"t{x}" for x in range(T)]
    col_names.append("Attack")
    data_frame = pd.DataFrame(data, columns=col_names)
    return data_frame


def generate_test_data_file(
    path,
    T,
    N,
    m_mean=1000,
    attack_percentage=0.1,
    attack_strength=100
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
    data = generate_test_data_df(
        T=T,
        N=N,
        m_mean=m_mean,
        attack_percentage=attack_percentage,
        attack_strength=attack_strength
    )
    data.to_csv(path)


if __name__ == "__main__":
    data = generate_test_data_df(T=5, N=10)
    path = r"test_data.csv"
    generate_test_data_file(path=path, T=100, N=200)
    print(data.head())
