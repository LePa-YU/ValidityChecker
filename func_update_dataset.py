from csv import DictReader
import pandas as pd
import numpy as np

def open_file(filepath):
    df = pd.read_csv(filepath, encoding="utf-8")
    df = df.rename(columns=lambda x: x.strip())
    df['identifier'] = df['identifier'].astype('Int64')
    df.set_index('identifier', inplace=True)

    return df

def save_file(df, filepath):
    file_location = filepath.split('.csv')[0]
    save_file_location = file_location + '_updated.csv'

    df.to_csv(save_file_location, encoding='utf-8')

def add_row(df):
    new_row = {
        "title": np.nan,
        "description": np.nan,
        "url": np.nan,
        "type": np.nan,
        "assesses": np.nan,
        "comesAfter": np.nan,
        "alternativeContent": np.nan,
        "requires": np.nan,
        "contains": np.nan,
        "isPartOf": np.nan,
        "isFormatOf": np.nan,
    }

    print("Do you want to: add to the end (e), add to specific index (i).")
    choice = input("input: ")
    match choice:
        case "e":
            # Add to the end of the dataframe, before the "end" node
            df.loc[df.tail(1).index.item() - 0.5] = new_row
            df = df.sort_index().reset_index(drop=True)
            identifier = df.tail(1).index.item() - 1
        case "i":
            print("Give index:")
            print("TBD")
            # shift_row(index, df, new_row)
            # index = input("input: ")
        case _:
            print("Did not catch that. Try again?")

    return update_row(df, identifier, new_row)

def edit(df):
    print("Please indicate what row you wish to edit.")
    identifier = input("Row ID:")
    new_row = {
        "title": df.at[int(identifier), "title"],
        "description": df.at[int(identifier), "description"],
        "url": df.at[int(identifier), "url"],
        "type": df.at[int(identifier), "type"],
        "assesses": df.at[int(identifier), "assesses"],
        "comesAfter": df.at[int(identifier), "comesAfter"],
        "alternativeContent": df.at[int(identifier), "alternativeContent"],
        "requires": df.at[int(identifier), "requires"],
        "contains": df.at[int(identifier), "contains"],
        "isPartOf": df.at[int(identifier), "isPartOf"],
        "isFormatOf": df.at[int(identifier), "isFormatOf"],
    }

    return update_row(df, identifier, new_row)

def update_row(df, identifier, new_row):
    print("")
    print("What do you wish to edit? Please, select one of the following: ")
    print("title (t), "
          "description (d), "
          "url (u), "
          "type (type), "
          "assesses (a), "
          "comesAfter (ca), "
          "alternativeContent (ac), "
          "requires (r), "
          "contains (c), "
          "isPartOf (ipo), "
          "isFormatOf (ifo), ")
    print("Do you want to see your current edits? Print (p), ",
          "Done with edits to ID: " + str(identifier) + ". Type (save) to save and exit or (cancel) to cancel and exit.")

    # input("Press enter to continue...")

    while True:
        edit_choice = input('input: ')
        match edit_choice:
            case "t":
                print("Change title.")
                new_row["title"] = input("Input: ")
            case "d":
                print("Change description")
                new_row["description"] = input("Input: ")
            case "u":
                print("Change URL")
                new_row["url"] = input("Input: ")
            case "type":
                print("Change type")
                new_row["type"] = input("Input:")
            case "a":
                print("Change assesses relation")
                new_row["assesses"] = input("Input: ")
            case "ca":
                print("Change comesAfter relation")
                new_row["comesAfter"] = input("Input: ")
            case "ac":
                print("Change alternativeContent relation")
                new_row["alternativeContent"] = input("Input: ")
            case "r":
                print("Change requires relation")
                new_row["requires"] = input("Input: ")
            case "c":
                print("Change contains relation")
                new_row["contains"] = input("Input: ")
            case "ipo":
                print("Change isPartOf relation")
                new_row["isPartOf"] = input("Input: ")
            case "ifo":
                print("Change isFormatOf relation")
                new_row["isFormatOf"] = input("Input: ")
            case "p":
                print(new_row)
            case "save":
                df = save_row(df, identifier, new_row)
                break
            case "cancel":
                break
            case _:
                print("Did not catch that. Try again?")

    # input("Press enter to continue...")
    return df

def save_row(df, identifier, new_row):
    print("Edit_row")
    df.at[int(identifier), "title"] = new_row["title"]
    df.at[int(identifier), "description"] = new_row["description"]
    df.at[int(identifier), "url"] = new_row["url"]
    df.at[int(identifier), "assesses"] = new_row["assesses"]
    df.at[int(identifier), "comesAfter"] = new_row["comesAfter"]
    df.at[int(identifier), "alternativeContent"] = new_row["alternativeContent"]
    df.at[int(identifier), "requires"] = new_row["requires"]
    df.at[int(identifier), "contains"] = new_row["contains"]
    df.at[int(identifier), "isPartOf"] = new_row["isPartOf"]
    df.at[int(identifier), "isFormatOf"] = new_row["isFormatOf"]

    return df

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
