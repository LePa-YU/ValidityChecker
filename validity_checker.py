import os
from csv import DictReader
import func_validity_checker as func
import func_helper as helper

import tkinter as tk
from tkinter.filedialog import askopenfilename

# Datastructure
# {ID1: { data for ID1 from CSV }, ID2: { data for ID2 from CSV } ... IDN: { data for IDN from CSV }}
def read_file(warning_list, header_list, complete_header_list):
    print("Please give a file: ")
    root = tk.Tk()
    root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filepath = askopenfilename()  # show an "Open" dialog box and return the path to the selected file

    if os.path.exists(filepath):
        with open(filepath, encoding="utf-8-sig") as csvfile:
            csv_reader = DictReader(csvfile)
            file_dict = {}
            header_list.header_original = [x.strip(' ') for x in csv_reader.fieldnames]
            fieldnames = ','.join(header_list.header_original).lower().replace(" ", "").split(",")

            if 'identifier' not in fieldnames:
                return 0, 0

            header_list.header_modified = fieldnames
            header_list.check_header(warning_list, complete_header_list)
            header_list.add_header(complete_header_list)
            csv_reader.fieldnames = header_list.header_modified

            empty_row = []
            empty_row_full = []

            for count, row in enumerate(csv_reader):
                try:
                    if (row['title'] == '' or row['title'] == None) and \
                            (row['description'] == '' or row['description'] == None) and \
                            (row['url'] == '' or row['url'] == None) and \
                            (row['type'] == '' or row['type'] == None) and \
                            (row['comesafter'] == '' or row['comesafter'] == None) and \
                            (row['alternativecontent'] == '' or row['alternativecontent'] == None) and \
                            (row['requires'] == '' or row['requires'] == None) and \
                            (row['ispartof'] == '' or row['ispartof'] == None) and\
                            (row['isformatof'] == '' or row['isformatof'] == None):
                        if row['identifier'] == '':
                            empty_row_full.append(str(count))
                        else:
                            empty_row.append(row['identifier'])

                    elif row['type'] == 'aER' or row['type'] == 'iER' or row['type'] == 'rER':
                        file_dict[row['identifier']] = func.Composite(row['identifier'], row['title'], row['description'], row['url'],
                                                           row['type'], row['assesses'], row['comesafter'],
                                                           row['alternativecontent'], row['requires'], row['ispartof'],
                                                           row['isformatof'])
                        file_dict[row['identifier']].confirm_fields(warning_list)
                    else:
                        file_dict[row['identifier']] = func.Atomic(row['identifier'], row['title'], row['description'], row['url'],
                                                           row['type'], row['assesses'], row['comesafter'],
                                                           row['alternativecontent'], row['requires'], row['ispartof'],
                                                           row['isformatof'])
                        file_dict[row['identifier']].confirm_fields(warning_list)
                except KeyError as ke:
                    print('Key ERROR: Please check that your csv header has the required fields. See: ', ke)
                    break
            # input("Press enter to continue...")
            if empty_row:
                text = helper.print_fields(empty_row)
                warning_list.add_warning("Warning: Empty row(s): " + text)
            if empty_row_full:
                text = helper.print_fields(empty_row_full)
                warning_list.add_warning("Warning: Empty row(s): " + text + ". Please make sure rows that are fully empty are deleted.")
    else:
        print("No file selected.")
        raise SystemExit

    return file_dict, warning_list



def main():
    complete_header_list = ['identifier', 'title', 'description', 'url', 'type', 'assesses', 'comesAfter',
                            'alternativeContent', 'requires', 'isPartOf', 'isFormatOf']
    warning_list = func.WarningList()
    header_list = func.Headerlist()
    file_dict, warning_list = read_file(warning_list, header_list, complete_header_list)

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

main()