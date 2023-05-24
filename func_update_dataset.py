from csv import DictReader
import pandas as pd
import numpy as np

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
            df.rename(index={index: str(new_index)}, inplace=True)
            df = df.replace(index, str(new_index))

            df = check_alt_list(df, str(index), str(new_index))

        old_index = new_index

    return df

def check_alt_list(df, old_index, new_index):
    for index, row in df.iterrows():
        try:
           if np.isnan(df.at[index, 'contains']):
            pass
        except:
            if old_index in df.loc[index,'contains']:
                # print(df.loc[index, 'contains'])
                df.loc[index,'contains'] = df.loc[index, 'contains'].replace(old_index, new_index)
                # print(df.loc[index,'contains'])
                # print("---")

    return df
