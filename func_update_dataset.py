from csv import DictReader
import pandas as pd


def open_file(filepath):
    df = pd.read_csv(filepath)
    df.set_index('identifier', inplace=True)
    return df


def save_file(df, filepath):
    file_location = filepath.split('.csv')[0]
    save_file_location = file_location + '_updated.csv'

    df.to_csv(save_file_location, encoding='utf-8')


def remove_empty_lines(df):
    df = df.dropna(how='all')
    return df


def shift_nodes_after_empty_lines(df):
    old_index = -1
    for index, row in df.iterrows():
        index_int = int(index)
        new_index = old_index + 1
        if index_int != new_index:
            print("Index out of sync")


            df.rename(index={index: str(new_index)}, inplace=True)
            df = df.replace(index, str(new_index))

            # print(index)
            # print(old_index)
            # print(row)
            # input("Press enter to continue...")

        old_index = new_index

    return df

# def move_nodes(df, shift, start):
#
#     for index, row in df.iterrows():
#         if index == start:
#
#             print("")
