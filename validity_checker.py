import os
from csv import DictReader
import func_validity_checker as func

import tkinter as tk
from tkinter.filedialog import askopenfilename

# Datastructure
# {ID1: { data for ID1 from CSV }, ID2: { data for ID2 from CSV } ... IDN: { data for IDN from CSV }}
def read_file(warning_list):
    print("Please give a file: ")
    root = tk.Tk()
    root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filepath = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    print(filepath)
    if os.path.exists(filepath):
        with open(filepath) as csvfile:
            csv_reader = DictReader(csvfile)
            file_dict = {}

            for row in csv_reader:
                try:
                    if row['type'] == 'aER' or row['type'] == 'iER' or row['type'] == 'rER':
                        file_dict[row['ID']] = func.Composite(row['ID'], row['title'], row['alternative'], row['targetUrl'],
                                                           row['type'], row['assesses'], row['comesAfter'],
                                                           row['alternativeContent'], row['requires'],
                                                           row['isRequiredBy'], row['isPartOf'], row['isFormatOf'], )
                        file_dict[row['ID']].confirm_fields(warning_list)
                    else:
                        file_dict[row['ID']] = func.Atomic(row['ID'], row['title'], row['alternative'], row['targetUrl'],
                                                              row['type'], row['assesses'], row['comesAfter'],
                                                              row['alternativeContent'], row['requires'],
                                                              row['isRequiredBy'], row['isPartOf'], row['isFormatOf'], )
                        file_dict[row['ID']].confirm_fields(warning_list)
                except KeyError as ke:
                    print('ERROR: Please check that your csv header does not have extra whitespace before or after the '
                          'terms listed. See: ', ke)

            # input("Press enter to continue...")
    else:
        raise FileNotFoundError('No such file or directory')

    return file_dict, warning_list

def main():
    warning_list = func.WarningList()
    list_dict, w_list = read_file(warning_list)

    while True:
        print_error = input('Do you want to print warning or error list? (Type: warning or error or quit) ')
        if print_error.lower() == 'warning' or print_error.lower() == 'w':
            if not w_list.print_warning():
                print("No warnings!")
            else:
                w_list.print_warning()
        elif print_error.lower() == 'error' or print_error.lower() == 'e':
            if not w_list.print_error():
                print("No errors!")
            else:
                w_list.print_error()
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

main()