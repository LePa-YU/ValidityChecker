import os
import func_update_dataset as updater
import func_validity_checker as func
import func_helper as helper

import tkinter as tk
from tkinter.filedialog import askopenfilename

import os


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


def save_temp_file(df, filepath):
    file_location = filepath.split('.csv')[0]
    save_file_location = file_location + '_temp.csv'
    df.to_csv(save_file_location, encoding='utf-8')


def delete_temp_file(filepath):
    file_location = filepath.split('.csv')[0]
    delete_file_location = file_location + '_temp.csv'
    os.remove(delete_file_location)

def validate(filepath):
    complete_header_list = ['identifier', 'title', 'description', 'url', 'type', 'assesses', 'comesAfter',
                            'alternativeContent', 'requires', 'isPartOf', 'isFormatOf']
    warning_list = func.WarningList()
    header_list = func.Headerlist()
    file_dict, warning_list = helper.open_file(warning_list, header_list, complete_header_list, filepath)

    if file_dict == 0 and warning_list == 0:
        print('Critical error in header. Please ensure they match the provided MAP document.')
        raise SystemExit

    helper.check_dict(file_dict, warning_list)

    return warning_list


# def main():
if __name__ == '__main__':
    filepath = read_file()
    df = updater.open_file(filepath)

    warning_list = validate(filepath)
    warning_list.print_msg()

    while True:
        print("#######################################")
        print("The following actions are available: ")
        print("Validity checker: ")
        print("   Validate (v). Print errors (e). Print warnings (w). Print empty fields (f).")
        print("Manipulate dataset:")
        print("   Delete empty rows (d). Add row (add). Delete row (del). Edit row (edit).")
        print("To print:")
        print("   Full dataset (p). Name view (n). Relationship view (r). Single ID (id).")
        print("Save dataset (s). Quit (q)")
        print("#######################################")
        choice_vc = input('Input:  ')
        match choice_vc:
            # Validity checker
            case "v" | "validate":
                file_location = filepath.split('.csv')[0]
                save_file_location = file_location + '_temp.csv'
                try:
                    warning_list = validate(save_file_location)
                except:
                    save_temp_file(df, filepath)
                    warning_list = validate(save_file_location)
                warning_list.print_msg()
            case "w":
                if not warning_list.warning:
                    print("No warnings!")
                    print("")
                else:
                    warning_list.print_warning()
                    print("")
            case "e":
                if not warning_list.error:
                    print("No errors!")
                    print("")
                else:
                    warning_list.print_error()
                    print("")
            case "f":
                if not warning_list.missing_fields:
                    print("No empty fields!")
                    print("")
                else:
                    warning_list.print_missing_fields()
                    print("")

            # Manipulate dataset
            case "d":
                print("Delete empty rows")
                df = updater.remove_empty_lines(df)
                df = updater.shift_nodes_after_empty_lines(df)
                save_temp_file(df, filepath)

            case "add":
                print("Add row")
                df = updater.add_row(df)
                save_temp_file(df, filepath)

            case "del":
                print("Delete row")
                to_delete = input('What row do you want to delete. Give Identifier:  ')
                df = updater.delete_row(df, int(to_delete))
                save_temp_file(df, filepath)

            case "edit":
                print("Edit row")
                df = updater.edit(df)
                save_temp_file(df, filepath)

            # Print dataset
            case "p":
                print(df.to_string())

            case "n":
                # identifier, title, description, url, type, assesses, comesAfter, alternativeContent, requires, isPartOf, isFormatOf
                print(df[['title']].to_string())

            case "r":
                print(df[['title', 'assesses', 'comesAfter', 'alternativeContent', 'requires', 'isPartOf', 'isFormatOf']].to_string())

            case "id":
                print_id = input("What ID do you want to print? ")
                print(df.loc[[int(print_id)]].to_string())

            # Save/Quit
            case "s":
                updater.save_file(df, filepath)

            case "q":
                print("Program exit.")
                delete_temp_file(filepath)
                raise SystemExit

            case _:
                print("Did not catch that. Try again?")
