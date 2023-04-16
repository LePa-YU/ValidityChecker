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
        warnings = print_fields(list)
        warning_comesAfter = print_fields(list_comesAfter)

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