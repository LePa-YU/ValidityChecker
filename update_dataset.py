import os
import func_update_dataset as helper
import tkinter as tk
from tkinter.filedialog import askopenfilename
import pandas as pd


# Datastructure
# {ID1: { data for ID1 from CSV }, ID2: { data for ID2 from CSV } ... IDN: { data for IDN from CSV }}
def read_file():
    print("Please give a file: ")
    root = tk.Tk()
    root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filepath = askopenfilename()  # show an "Open" dialog box and return the path to the selected file

    if os.path.exists(filepath):
        return filepath
    else:
        print("No file selected.")
    raise SystemExit


# def main():
if __name__ == '__main__':
    filepath = read_file()
    file_df = helper.open_file(filepath)

    # file_df = helper.remove_empty_lines(file_df)
    # file_df = helper.shift_nodes_after_empty_lines(file_df)
    # helper.save_file(file_df, filepath)

    while True:
        print("The following actions are available: ")
        print("Options: Continue (c), Delete empty rows (d), Print dataset (p), Validate (v), Quit (q)")
        choice = input('Input:  ')
        match choice:
            case "c":
                print("Temporary command until validate works.")
                break
            case "d":
                print("Delete empty rows")
                file_df = helper.remove_empty_lines(file_df)
                file_df = helper.shift_nodes_after_empty_lines(file_df)
            case "p":
                print(file_df.to_string())
            case "v":
                print("Validate dataset")
                print("TBD")
            case "q":
                print("Program exit.")
                raise SystemExit
            case _:
                print("Did not catch that. Try again?")

    while True:
        print("The following actions are available: ")
        print("Options: Add row (a), Delete row (d), Edit row (e), Print dataset (p), Save dataset (s), Validate (v), "
              "Quit (q)")
        choice = input('Input:  ')
        match choice:
            case "a":
                print("Add row")
                file_df = helper.add_row(file_df)

            case "d":
                print("Delete row")
                to_delete = input('What row do you want to delete. Give Identifier:  ')
                file_df = helper.delete_row(file_df, to_delete)

            case "e":
                print("Edit row")
                file_df = helper.edit(file_df)

            case "p":
                print(file_df.to_string())

            case "s":
                helper.save_file(file_df, filepath)

            case "v":
                print("Validate dataset")
                print("TBD")

            case "q":
                print("Program exit.")
                raise SystemExit

            case _:
                print("Did not catch that. Try again?")
