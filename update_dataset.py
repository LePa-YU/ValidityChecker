import os
import func_update_dataset as helper
import tkinter as tk
from tkinter.filedialog import askopenfilename


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
    file_dict = helper.open_file(filepath)

    file_dict = helper.remove_empty_lines(file_dict)
    file_dict = helper.shift_nodes_after_empty_lines(file_dict)

    print(file_dict)

    # input("Press enter to continue...")

    helper.save_file(file_dict,filepath)

    while True:
        print("The following actions are available: ")
        print("Update (u). Quit (q).")
        choice = input('Input:  ')
        if choice.lower() == 'update' or choice.lower() == 'u':
            print("")

        elif choice.lower() == 'quit' or choice.lower() == 'q':
            print("Program exit.")
            raise SystemExit
        else:
            print("Did not catch that. Try again?")
