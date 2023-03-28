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