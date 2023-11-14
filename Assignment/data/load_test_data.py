import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


def load_test_data_file(dir: str):
    combined_df = pd.DataFrame()
    directory = os.path.join(os.getcwd(), dir)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):

                file_path = os.path.join(root, file)
                curr_df = pd.read_csv(file_path,
                                      usecols=['LCLid', 'energy(kWh/hh)'],
                                      low_memory=False,
                                      na_values='Null')

                concatenated_df = curr_df.groupby('LCLid').apply(concatenate_readings)
                result_df = pd.DataFrame([concatenated_df], columns=concatenated_df.index)
                df_transposed = result_df.T

                expanded_df = pd.DataFrame(df_transposed[0].values.tolist(), index=df_transposed.index)
                expanded_df = expanded_df.fillna(0)

                for i in expanded_df.columns:
                    expanded_df[i] = expanded_df[i].apply(lambda x: int(x * 1000))

                combined_df = pd.concat([combined_df, expanded_df], axis=0)
                print(file)

    print(combined_df.shape)
    combined_df.to_csv('out.csv', index=True)
    return combined_df


def concatenate_readings(group):
    concatenated_readings = group.drop('LCLid', axis=1).values.flatten().tolist()
    return concatenated_readings


def find_closest_numbers(numbers, N):
    if N > len(numbers):
        raise ValueError("N cannot be larger than the length of the list")

    # Sort the list while keeping track of original indexes
    sorted_numbers_with_index = sorted((val, idx) for idx, val in enumerate(numbers))

    # Initialize the minimum difference to a large number
    min_diff = float('inf')
    start_index = 0

    # Iterate to find the N consecutive numbers with the smallest range
    for i in range(len(numbers) - N + 1):
        diff = sorted_numbers_with_index[i + N - 1][0] - sorted_numbers_with_index[i][0]
        if diff < min_diff:
            min_diff = diff
            start_index = i

    # Retrieve the original indexes of the closest numbers
    closest_indexes = [sorted_numbers_with_index[i][1] for i in range(start_index, start_index + N)]

    return closest_indexes


def load_data(
        num_readings: int = 100,
        num_smart_meters: int = 100,
        attack_percentage=0.1,
        mean_diff=100,
        deviation_diff=1
):
    ids = ['MAC000002',
           'MAC003613',
           'MAC003597',
           'MAC003579',
           'MAC003566',
           'MAC003557',
           'MAC003553',
           'MAC003482',
           'MAC003463',
           'MAC003449',
           'MAC003428',
           'MAC003423',
           'MAC003422',
           'MAC003400',
           'MAC003394',
           'MAC003388',
           'MAC003348',
           'MAC000246',
           'MAC003305',
           'MAC003281',
           'MAC003252',
           'MAC003239',
           'MAC003646',
           'MAC003656',
           'MAC003668',
           'MAC003680',
           'MAC004431',
           'MAC004387',
           'MAC004319',
           'MAC004247',
           'MAC004179',
           'MAC004034',
           'MAC003874',
           'MAC003863',
           'MAC003856',
           'MAC003851',
           'MAC003223',
           'MAC003844',
           'MAC003826',
           'MAC003817',
           'MAC003805',
           'MAC003775',
           'MAC003740',
           'MAC003737',
           'MAC003719',
           'MAC003718',
           'MAC003686',
           'MAC000450']

    num_readings = max(10, num_readings)
    num_smart_meters = max(10, num_smart_meters)
    num_bad_actors = int(num_readings * attack_percentage)

    df = pd.read_csv("out.csv", nrows=5*num_readings+1)
    matrix = df.iloc[:, 1:len(ids) + 1].values

    means = []

    for line in range(matrix.shape[0]):  # matrix.shape[1] gives the number of columns
        means.append(np.mean(matrix[line, :]))

    closest_indexes = find_closest_numbers(means, num_smart_meters)
    matrix_used = []

    for index in closest_indexes:
        matrix_used.append(matrix[index])

    deviations = []
    for col in range(matrix.shape[1]):  # matrix.shape[1] gives the number of columns
        means.append(np.mean(matrix[:, col]))
        deviations.append(np.std(matrix[:, col]))

    mean = means[0]
    std_dev = deviations[0]

    x = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 1000)

    #
    # for i in range(num_bad_actors):
    #     modification = np.random.normal(loc=attack_strength)
    #     if is_stealing == 1:
    #         value -= modification
    #     else:
    #         value += modification
    #     if i % 2 == 0:
    #
    #         # TODO Generate malfunctioning
    #     else:
    #         # TODO Generate stealing


if __name__ == "__main__":
    dir = "halfhourly_dataset"
    load_data()
