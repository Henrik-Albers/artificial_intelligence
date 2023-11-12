import pandas as pd
import os


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


if __name__ == "__main__":
    dir = "halfhourly_dataset"
    data = load_test_data_file(dir)
    # data = pd.read_csv("out.csv")
