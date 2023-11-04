import numpy as np
import pandas as pd


def generate_test_data_df(
    T,
    N,
    m_mean=10,
    attack_probability=0.1,
    stealing_probability=0.5,
    attack_strength=5
):
    data = []
    for record_idx in range(N):
        record = []
        # Attack happened
        is_attacker = np.random.choice(
            [0, 1], p=[1-attack_probability, attack_probability])
        # Steal or malfunction
        is_stealing = np.random.choice(
            [0, 1], p=[1-stealing_probability, stealing_probability])
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
                record.append("stealing")
            else:
                record.append("malfunctioning")
        else:
            record.append("sm ok")
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
    attack_probability=0.1,
    stealing_probability=0.5,
    attack_strength=5
):
    data = generate_test_data_df(
        T=T,
        N=N,
        m_mean=m_mean,
        attack_probability=attack_probability,
        stealing_probability=stealing_probability,
        attack_strength=attack_strength
    )
    data.to_csv(path)


if __name__ == "__main__":
    data = generate_test_data_df(T=5, N=10)
    path = r"Assignment\data\test_data.csv"
    generate_test_data_file(path=path, T=5, N=10)
    print(data.head())
