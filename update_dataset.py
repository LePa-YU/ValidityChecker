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
    try:
        file_location = filepath.split('.csv')[0]
        delete_file_location = file_location + '_temp.csv'
        os.remove(delete_file_location)
    except:
        return 0

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

def formatting(text):
    print("#######################################")
    print("")
    print(text)
    print("")
    print("#######################################")

# def main():
if __name__ == '__main__':
    filepath = read_file()
    df = updater.open_file(filepath)

    warning_list = validate(filepath)
    print("#######################################")
    print("")
    warning_list.print_msg()
    print("")
    print("#######################################")


    delete_temp_file(filepath)



    while True:
        # print("#######################################")
        print("The following actions are available: ")
        print("Validity checker: ")
        print("   Validate (v). Print errors (e). Print warnings (w). Print empty fields (f).")
        print("Manipulate dataset:")
        print("   Delete empty rows (d). Add row (add). Delete row (del). Edit row (edit).")
        print("To print:")
        print("   Full dataset (p). Name view (n). Relationship view (r). Single ID (id).")
        print("Save dataset (s). Quit (q)")
        # print("#######################################")
        choice_vc = input('>>Input:  ')
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
                print("#######################################")
                print("")
                warning_list.print_msg()
                print("")
                print("#######################################")
                delete_temp_file(filepath)

            case "w" | "warning":
                if not warning_list.warning:
                    formatting("No warnings!")
                else:
                    print("#######################################")
                    print("")
                    warning_list.print_warning()
                    print("")
                    print("#######################################")
            case "e" | "error":
                if not warning_list.error:
                    formatting(("No errors!"))
                else:
                    print("#######################################")
                    print("")
                    warning_list.print_error()
                    print("")
                    print("#######################################")
            case "f" | "fields":
                if not warning_list.missing_fields:
                    formatting("No empty fields!")
                else:
                    print("#######################################")
                    print("")
                    warning_list.print_missing_fields()
                    print("")
                    print("#######################################")

            # Manipulate dataset
            case "d" | "delete":
                formatting("Deleting empty rows")

                df = updater.remove_empty_lines(df)
                df = updater.shift_nodes_after_empty_lines(df)
                save_temp_file(df, filepath)
                warning_list.empty_rows_deleted()

            case "add":
                if warning_list.empty_rows:
                    formatting("Please make sure empty rows are deleted.")
                else:
                    formatting("Add row")

                    df = updater.add_row(df)
                    save_temp_file(df, filepath)

            case "del":
                if warning_list.empty_rows:
                    formatting("Please make sure empty rows are deleted.")
                else:
                    formatting("Delete row")
                    to_delete = input('>>What row do you want to delete. Give Identifier:  ')
                    df, check = updater.delete_row(df, int(to_delete))
                    if check is True:
                        save_temp_file(df, filepath)
                    else:
                        formatting("Double check which node you're trying to delete.")

            case "edit":
                if warning_list.empty_rows:
                    formatting("Please make sure empty rows are deleted.")
                else:
                    formatting("Edit row")
                    df = updater.edit(df)
                    save_temp_file(df, filepath)

            # Print dataset
            case "p" | "print":
                formatting(df.to_string())

            case "n" | "name":
                # identifier, title, description, url, type, assesses, comesAfter, alternativeContent, requires, isPartOf, isFormatOf
                formatting(df[['title']].to_string())

            case "r" | "relationship":
                formatting(df[['title', 'assesses', 'comesAfter', 'alternativeContent', 'requires', 'isPartOf', 'isFormatOf']].to_string())

            case "id" | "ID":
                print_id = input(">>What ID do you want to print? ")
                formatting(df.loc[[int(print_id)]].to_string())

            # Save/Quit
            case "s" | "save":
                updater.save_file(df, filepath)

            case "q" | "quit" | "exit":
                formatting("Program exit.")
                delete_temp_file(filepath)
                raise SystemExit

            case _:
                formatting("Did not catch that. Try again?")
