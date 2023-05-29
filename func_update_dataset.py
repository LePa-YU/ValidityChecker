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

# identifier, title, description, url, type, assesses, comesAfter, alternativeContent, requires, contains, isPartOf, isFormatOf
def delete_row(df, id):
    id = int(id)
    df = delete_relationship(df, id)
    df = df.drop(id)
    df = shift_nodes_after_empty_lines(df)
    return df

def delete_relationship(df, id):
    df = df.replace(id, np.nan)
    df = delete_relationship_lists(df, id)

    return df

def delete_relationship_lists(df, id):
    for index, row in df.iterrows():
        try:
            if np.isnan(df.at[index, 'contains']):
                pass
        except:
            df.loc[index,'contains'] = df.loc[index, 'contains'].replace(str(id), np.nan)

        try:
            if np.isnan(df.at[index, 'requires']):
                pass
        except:
            df.loc[index, 'requires'] = df.loc[index, 'requires'].replace(str(id), np.nan)

    return df

def shift_nodes_after_empty_lines(df):
    old_index = -1
    change = False
    for index, row in df.iterrows():
        index_int = int(index)
        new_index = old_index + 1

        if index_int != new_index:
            change = True
            df.rename(index={index: str(new_index)}, inplace=True)
            df = df.replace(index, str(new_index))

            df = check_alt_list(df, str(index), str(new_index))

        old_index = new_index

    if change:
        print("Changed index of node(s).")

    return df

def check_alt_list(df, old_index, new_index):
    for index, row in df.iterrows():
        try:
            if np.isnan(df.at[index, 'contains']):
                pass
        except:
            if old_index in df.loc[index,'contains']:
                df.loc[index,'contains'] = df.loc[index, 'contains'].replace(old_index, new_index)
    return df
