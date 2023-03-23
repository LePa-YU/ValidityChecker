import os
from csv import DictReader
import func_validity_checker as func

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
            header_list.header_original = csv_reader.fieldnames
            fieldnames = ','.join(csv_reader.fieldnames).lower().replace(" ", "").split(",")

            if 'identifier' not in fieldnames:
                return 0, 0

            header_list.header_modified = fieldnames
            header_list.check_header(warning_list, complete_header_list)
            header_list.add_header(complete_header_list)


            csv_reader.fieldnames = header_list.header_modified

            for row in csv_reader:
                try:
                    if row['type'] == 'aER' or row['type'] == 'iER' or row['type'] == 'rER':
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
    else:
        print("No file selected.")
        raise SystemExit

    return file_dict, warning_list

def check_dict(file_dict, warning_list):
    for key, er in file_dict.items():
        confirm_relationships(key, er, warning_list)
        confirm_disconnected_node(file_dict, key, er, warning_list)

# CONFIRM_RELATIONSHIPS
# Issue warning if a relationship is missing \\DEPRICATED since isRequiredBy is removed
# Check for circular logic in relationships: requires
# Check for iER, aER, rER relationships
## iER, aER must have a requires or comesAfter
## rER must have an assesses relationship
def confirm_relationships(key, er, warning_list):
    # for key, er in file_dict.items():
    # if er.requires:
    #     list = er.requires.replace(" ", "").split(",")
    #     for n in list:
    #         if key not in file_dict[n].isRequiredBy:
    #             warning_list.add_warning("Warning: Missing relationship (isRequiredBy) in "+file_dict[n].id+" for "+key)
    # elif er.isRequiredBy:
    #     list = er.isRequiredBy.replace(" ","").split(",")
    #     for n in list:
    #         if key not in file_dict[n].requires:
    #             warning_list.add_warning("Warning: Missing relationship (requires) in "+file_dict[n].id+" for "+key)

    if er.type == 'aER' or er.type == 'iER':
        if er.requires == '' and er.comesAfter == '':
            warning_list.add_warning("Warning: Missing relationship (requires or comesAfter) for ID: " + key)

    elif er.type == 'rER':
        if er.assesses == '':
            warning_list.add_warning("Warning: Missing relationship (assesses) for ID: " + key)

    # input("Press enter to continue...")



# assesses,comesAfter,alternativeContent,requires,isPartOf,isFormatOf
def confirm_disconnected_node(file_dict, key, er, warning_list):
    # print(er.requires)
    check = False
    if not er.requires and not er.assesses and not er.comesAfter and not er.alternativeContent and not er.isPartOf \
            and not er.isFormatOf:
        for key2, er2 in file_dict.items():
            if er2.requires is file_dict[key].identifier is file_dict[key].identifier or er2.assesses is file_dict[key].identifier or er2.comesAfter \
                is file_dict[key].identifier or er2.alternativeContent is file_dict[key].identifier or er2.isPartOf is file_dict[key].identifier \
                or er2.isFormatOf is file_dict[key].identifier:
                check = True
                break
        if check is False and er.title != 'End' and er.title != 'Start':
            warning_list.add_warning("Warning: No relationships found for ID: "+file_dict[key].identifier)



def main():
    complete_header_list = ['identifier', 'title', 'description', 'url', 'type', 'assesses', 'comesAfter',
                            'alternativeContent', 'requires', 'isPartOf', 'isFormatOf']
    warning_list = func.WarningList()
    header_list = func.Headerlist()
    file_dict, warning_list = read_file(warning_list, header_list, complete_header_list)

    if file_dict == 0 and warning_list == 0:
        print('Critical error in header. Please ensure they match the MAP document.')
        raise SystemExit

    check_dict(file_dict, warning_list)

    # input("Press enter to continue...")

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