import os

import func_validity_checker as func
import func_helper as helper

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
    complete_header_list = ['identifier', 'title', 'description', 'url', 'type', 'assesses', 'comesAfter',
                            'alternativeContent', 'requires', 'isPartOf', 'isFormatOf']
    warning_list = func.WarningList()
    header_list = func.Headerlist()
    filepath = read_file()
    file_dict, warning_list = helper.open_file(warning_list, header_list, complete_header_list, filepath)

    if file_dict == 0 and warning_list == 0:
        print('Critical error in header. Please ensure they match the provided MAP document.')
        raise SystemExit

    helper.check_dict(file_dict, warning_list)

    while True:
        warning_list.print_msg()
        print("The following actions are available: ")
        print("Print errors (e). Print warnings (w). Print empty fields (f). Quit (q).")
        print_error = input('Input:  ')
        if print_error.lower() == 'warning' or print_error.lower() == 'w':
            if not warning_list.warning:
                print("No warnings!")
                print("")
            else:
                warning_list.print_warning()
                print("")
        elif print_error.lower() == 'error' or print_error.lower() == 'e':
            if not warning_list.error:
                print("No errors!")
                print("")
            else:
                warning_list.print_error()
                print("")
        elif print_error.lower() == 'field' or print_error.lower() == 'f':
            if not warning_list.missing_fields:
                print("No empty fields!")
                print("")
            else:
                warning_list.print_missing_fields()
                print("")
        elif print_error.lower() == 'quit' or print_error.lower() == 'q':
            print("Program exit.")
            raise SystemExit
        else:
            print("Did not catch that. Try again?")

        # while True:
        #     exit_or_continue = input('Do you wish to continue with a new file? (Yes/No): ')
        #     if exit_or_continue.lower() == 'yes' or exit_or_continue.lower() == 'y':
        #         warning_list = func.WarningList()
        #         list_dict, w_list = read_file(warning_list)
        # elif exit_or_continue.lower() == 'no' or exit_or_continue.lower() == 'n':
        #     print("Program exit.")
        #     raise SystemExit
        # else:
        #     print("Did not catch that. Try again?")

# main()