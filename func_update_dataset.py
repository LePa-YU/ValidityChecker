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

    print("The add function will add a new line to the end of the file.")
    # print(df.tail(1).index.item())
    # print(float(df.tail(1).index.item()) - 0.5)

    df.loc[int(df.tail(1).index.item()) - 0.5] = new_row
    # print(df.to_string())

    df = df.sort_index().reset_index(drop=True)
    identifier = df.tail(1).index.item() - 1

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
          # "contains (c), "
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
                new_row["title"] = input("title: ")
            case "d":
                print("Change description")
                new_row["description"] = input("description: ")
            case "u":
                print("Change URL")
                new_row["url"] = input("URL: ")
            case "type":
                print("Change type")
                new_row["type"] = input("type:")
            case "a":
                print("Change assesses relation")
                new_row["assesses"] = input("assesses: ")
            case "ca":
                print("Change comesAfter relation")
                new_row["comesAfter"] = input("comesAfter: ")
            case "ac":
                print("Change alternativeContent relation")
                new_row["alternativeContent"] = input("alternativeContent: ")
            case "r":
                print("Change requires relation")
                new_row["requires"] = input("requires: ")
            # case "c":
            #     print("Change contains relation")
            #     new_row["contains"] = input("contains: ")
            case "ipo":
                print("Change isPartOf relation")
                new_row["isPartOf"] = input("isPartOf: ")
            case "ifo":
                print("Change isFormatOf relation")
                new_row["isFormatOf"] = input("isFormatOf: ")
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
    # df.at[int(identifier), "contains"] = new_row["contains"]
    df.at[int(identifier), "isPartOf"] = new_row["isPartOf"]
    df.at[int(identifier), "isFormatOf"] = new_row["isFormatOf"]

    return df

def remove_empty_lines(df):
    df = df.dropna(how='all')

    return df

# identifier, title, description, url, type, assesses, comesAfter, alternativeContent, requires, contains, isPartOf, isFormatOf
def delete_row(df, identifier):
    identifier = float(identifier)
    df = delete_relationship(df, identifier)
    df = df.drop(identifier)
    df = shift_nodes_after_empty_lines(df)
    return df

def delete_relationship(df, id):
    df = df.replace(id, np.nan)
    df = delete_relationship_lists(df, id)

    return df

def delete_relationship_lists(df, id):
    for index, row in df.iterrows():
        # try:
        #     if np.isnan(df.at[index, 'contains']):
        #         pass
        # except:
        #     df.loc[index,'contains'] = df.loc[index, 'contains'].replace(str(id), np.nan)

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
        index_int = float(index)
        new_index = old_index + 1

        if index_int != new_index:
            change = True
            df.rename(index={index: new_index}, inplace=True)
            df = df.replace(index, str(new_index))

            # df = check_alt_list(df, str(index), str(new_index))

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
