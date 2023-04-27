import func_validity_checker as func
from csv import DictReader
def open_file(warning_list, header_list, complete_header_list, filepath):
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
            text = print_fields(empty_row)
            warning_list.add_warning("Warning: Empty row(s): " + text)
        if empty_row_full:
            text = print_fields(empty_row_full)
            warning_list.add_warning("Warning: Empty row(s): " + text + ". Please make sure rows that are fully empty are deleted.")

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
    if er.oer_type == 'aER' or er.oer_type == 'iER':
        if er.requires == '' and er.comesAfter == '':
            warning_list.add_warning("Warning: Missing relationship (requires or comesAfter) for ID: " + key)

    elif er.oer_type == 'rER':
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
def confirm_start_end_nodes(key, er, warning_list, node, oer_type):
    list = []
    list_comesAfter = []
    if er.oer_type.lower() == oer_type and node is not False:
        warning_list.add_error("ERROR: There can only be one " + oer_type +" node.")
    elif er.oer_type.lower() == oer_type:

        node = er.identifier
        list, comesAfter, list_comesAfter = check_if_field_exists(er, list, list_comesAfter)
        warnings = print_fields(list)
        warning_comesAfter = print_fields(list_comesAfter)

        if warning_comesAfter:
            if oer_type == 'end' and er.comesAfter and len(warnings) == 0:
                pass
            else:
                if oer_type == 'end' and len(warnings) > 0:
                    warning_list.add_error(
                        "ERROR: The " + oer_type + " node should not have any other relationships. Check the following: " + warnings + " on row ID: " + er.identifier + ". Exceptions are Start node comesBefore and End node comesAfter.")
                else:
                    warning_list.add_error("ERROR: The " +oer_type+ " node should not have any other relationships. Check the following: " + warning_comesAfter + " on row ID: "+er.identifier + ". Exceptions are Start node comesBefore and End node comesAfter.")

    return node

# def check_field_type(file_dict, key, er, warning_list):
#     TODO



def check_if_field_exists(er, er_list, list_comesAfter):
    comesAfter = False
    if er.assesses != '':
        er_list.append('assesses')
        list_comesAfter.append('assesses')
    if er.comesAfter != '':
        list_comesAfter.append('comesAfter')
        comesAfter = True
    if er.alternativeContent != '':
        er_list.append('alternativeContent')
        list_comesAfter.append('alternativeContent')
    if er.requires != '':
        er_list.append('requires')
        list_comesAfter.append('requires')
    if er.isPartOf != '':
        er_list.append('isPartOf')
        list_comesAfter.append('isPartOf')
    if er.isFormatOf != '':
        er_list.append('isFormatOf')
        list_comesAfter.append('isFormatOf')

    return er_list, comesAfter, list_comesAfter

def print_fields(fieldname):
    text = ''
    first = False
    for idx, x in enumerate(fieldname):
        if idx == 0 and len(fieldname) > 1 and first is False:
            text = x + ", "
        elif first is False:
            text = x

        if idx < len(fieldname) - 1 and first is True:
            text = text + x + ", "
        if idx == len(fieldname) - 1 and first is True:
            text = text + x

        first = True
    return text