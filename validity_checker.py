import os
from csv import DictReader
import func_validity_checker as func
import func_helper as helper

import tkinter as tk
from tkinter.filedialog import askopenfilename

# TODO: Spellcheck remove white space
# TODO: Warning for empty lines - remove from other checks


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

            for row in csv_reader:
                try:
                    # print(row)
                    # input("Press enter to continue...")

                    if row['title'] == '' and row['description'] == '' and row['url'] == '' and row['type'] == '' and row['comesafter'] == '' and row['alternativecontent'] == '' and row['requires'] == '' and row['ispartof'] == '' and row['isformatof'] == '':
                        empty_row.append(row['identifier'])
                        # warning_list.add_warning('Warning: the following row is empty. ID: '+row['identifier'])

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
    else:
        print("No file selected.")
        raise SystemExit

    return file_dict, warning_list

def check_dict(file_dict, warning_list):
    # TODO: make sure that list of errors is in order
    start_node = False
    end_node = False
    for key, er in file_dict.items():
        confirm_relationships(key, er, warning_list)
        confirm_disconnected_node(file_dict, key, er, warning_list)
        start_node = confirm_start_end_nodes(key, er, warning_list, start_node, 'start')
        end_node = confirm_start_end_nodes(key, er, warning_list, end_node, 'end')

# CONFIRM_RELATIONSHIPS
# Issue warning if a relationship is missing \\DEPRICATED since isRequiredBy is removed
# TODO Check for circular logic in relationships: requires
# Check for iER, aER, rER relationships
## iER, aER must have a requires or comesAfter
## rER must have an assesses relationship
def confirm_relationships(key, er, warning_list):
    if er.type == 'aER' or er.type == 'iER':
        if er.requires == '' and er.comesAfter == '':
            warning_list.add_warning("Warning: Missing relationship (requires or comesAfter) for ID: " + key)

    elif er.type == 'rER':
        if er.assesses == '':
            warning_list.add_warning("Warning: Missing relationship (assesses) for ID: " + key)

# assesses,comesAfter,alternativeContent,requires,isPartOf,isFormatOf
def confirm_disconnected_node(file_dict, key, er, warning_list):
    # print(er.requires)
    check = False
    if not er.requires and not er.assesses and not er.comesAfter and not er.alternativeContent and not er.isPartOf \
            and not er.isFormatOf:
        for key2, er2 in file_dict.items():
            if er2.requires is file_dict[key].identifier is file_dict[key].identifier or er2.assesses is file_dict[key].identifier \
                    or er2.comesAfter is file_dict[key].identifier or er2.alternativeContent is file_dict[key].identifier \
                    or er2.isPartOf is file_dict[key].identifier or er2.isFormatOf is file_dict[key].identifier:
                check = True
                break
        if check is False and er.title != 'End' and er.title != 'Start':
            warning_list.add_warning("Warning: No relationships found for ID: "+file_dict[key].identifier)


# Confirm if a start or end node exists
def confirm_start_end_nodes(key, er, warning_list, node, type):
    list = []
    list_comesAfter = []
    if er.type.lower() == type and node is not False:
        warning_list.add_error("ERROR: There can only be one " + type +" node.")
    elif er.type.lower() == type:

        node = er.identifier
        list, comesAfter, list_comesAfter = check_if_field_exists(er, list, list_comesAfter)
        warnings = helper.print_fields(list)
        warning_comesAfter = helper.print_fields(list_comesAfter)

        if warning_comesAfter:
            if type == 'end' and er.comesAfter and len(warnings) == 0:
                pass
            else:
                if type == 'end' and len(warnings) > 0:
                    warning_list.add_error(
                        "ERROR: The " + type + " node should not have any other relationships. Check the following: " + warnings + " on row ID: " + er.identifier + ". Exceptions are Start node comesBefore and End node comesAfter.")
                else:
                    warning_list.add_error("ERROR: The " +type+ " node should not have any other relationships. Check the following: " + warning_comesAfter + " on row ID: "+er.identifier + ". Exceptions are Start node comesBefore and End node comesAfter.")

    return node

def check_if_field_exists(er, list, list_comesAfter):
    comesAfter = False
    if er.assesses != '':
        list.append('assesses')
        list_comesAfter.append('assesses')
    if er.comesAfter != '':
        list_comesAfter.append('comesAfter')
        comesAfter = True
    if er.alternativeContent != '':
        list.append('alternativeContent')
        list_comesAfter.append('alternativeContent')
    if er.requires != '':
        list.append('requires')
        list_comesAfter.append('requires')
    if er.isPartOf != '':
        list.append('isPartOf')
        list_comesAfter.append('isPartOf')
    if er.isFormatOf != '':
        list.append('isFormatOf')
        list_comesAfter.append('isFormatOf')

    return list, comesAfter, list_comesAfter

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