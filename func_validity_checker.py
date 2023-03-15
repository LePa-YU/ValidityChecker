class WarningList:
    def __init__(self):
        self.warning = []
        self.error = []
        self.missing_fields = []

    def add_error(self, error):
        self.error.append(error)

    def add_warning(self, warning):
        self.warning.append(warning)

    def add_missing_field(self, warning):
        self.missing_fields.append(warning)

    def print_error(self):
        for idx, x in enumerate(self.error):
            print(str(idx+1) + " " + x)

    def print_warning(self):
        for idx, x in enumerate(self.warning):
            print(str(idx+1)+" "+x)

    def print_missing_fields(self):
        for idx, x in enumerate(self.missing_fields):
            print(str(idx+1) + " " + x)

    def print_msg(self):
        print("There are "+str(len(self.error))+" errors, "+str(len(self.warning))+" warnings, and " +
              str(len(self.missing_fields))+" empty fields.")


class Headerlist:
    def __init__(self):
        self.header_modified = []
        self.header_original = []

    def add_header(self, real_header):
        for header in real_header:
            if header.lower() not in self.header_modified:
                self.header_modified.append(header.lower())

    def check_header(self, warning_list, real_header):
        error = []
        warning = []
        spelling = []
        for header in real_header:
            if (header.lower() not in self.header_modified) and (
                    header.lower() == 'id' or header.lower() == 'title' or header.lower() == 'type'):
                error.append(header)
            elif header.lower() not in self.header_modified:
                warning.append(header)
            elif header not in self.header_original:
                spelling.append(header)

        if error:
            text = self.print_columns(error)
            warning_list.add_error("ERROR: Missing column(s): "+text)
        if warning:
            text = self.print_columns(warning)
            warning_list.add_warning("Warning: Missing column(s): "+text)
        if spelling:
            text = self.print_columns(spelling)
            warning_list.add_warning("Warning: Check spelling: "+text)


    def print_columns(self, error):
        text = ''
        first = False
        for idx, x in enumerate(error):
            if idx == 0 and len(error) > 1 and first is False:
                text = x + ", "
            elif first is False:
                text = x

            if idx < len(error) - 1 and first is True:
                text = text + x + ", "
            if idx == len(error) - 1 and first is True:
                text = text + x

            first = True
        return text
class Atomic:
    def __init__(self, id, title, alternative, targetUrl, type, assesses, comesAfter, alternativeContent, requires,
                 isRequiredBy, isPartOf, isFormatOf):
        self.id = id
        self.title = title
        self.alternative = alternative
        self.targetUrl = targetUrl
        self.type = type
        self.assesses = assesses
        self.comesAfter = comesAfter
        self.alternativeContent = alternativeContent
        self.requires = requires
        self.isRequiredBy = isRequiredBy
        self.isPartOf = isPartOf
        self.isFormatOf = isFormatOf

    def confirm_fields(self, warning_list):
        list_error = []
        list_warning = []
        if self.alternative is not None:
            if len(self.id) == 0:
                list_error.append('ID')
                # warning_list.add_error("ERROR: Missing ID. ")
        if self.title is not None:
            if len(self.title) == 0:
                list_error.append('title')
                # warning_list.add_error("ERROR: Missing title in " + self.id)
        if self.type is not None:
            if len(self.type) == 0:
                list_error.append('type')
                # warning_list.add_error("ERROR: Missing type in " + self.id)

        if self.alternative is not None:
            if len(self.alternative) == 0:
                list_warning.append('alternative')
                # warning_list.add_missing_field("Missing field: alternative in " + self.id)
        if self.targetUrl is not None:
            if len(self.targetUrl) == 0:
                list_warning.append('targetUrl')
                # warning_list.add_missing_field("Missing field: URL in " + self.id)
        if self.assesses is not None:
            if len(self.assesses) == 0:
                list_warning.append('assesses')
                # warning_list.add_missing_field("Missing field: assesses relationships in " + self.id)
        if self.comesAfter is not None:
            if len(self.comesAfter) == 0:
                list_warning.append('comesAfter')
                # warning_list.add_missing_field("Missing field: comesAfter relationships in " + self.id)
        if self.alternativeContent is not None:
            if len(self.alternativeContent) == 0:
                list_warning.append('alternativeContent')
                # warning_list.add_missing_field("Missing field: alternativeContent relationships in " + self.id)
        if self.requires is not None:
            if len(self.requires) == 0:
                list_warning.append('requires')
                # warning_list.add_missing_field("Missing field: requires relationships in " + self.id)
        if self.isRequiredBy is not None:
            if len(self.isRequiredBy) == 0:
                list_warning.append('isRequiredBy')
                # warning_list.add_missing_field("Missing field: isRequiredBy relationships in " + self.id)
        if self.isPartOf is not None:
            if len(self.isPartOf) == 0:
                list_warning.append('isPartOf')
                # warning_list.add_missing_field("Missing field: isPartOf relationships in " + self.id)
        if self.isFormatOf is not None:
            if len(self.isFormatOf) == 0:
                list_warning.append('isFormatOf')
                # warning_list.add_missing_field("Warning: Missing isFormatOf relationships in " + self.id)

        error = self.print_fields(list_error)
        warning = self.print_fields(list_warning)

        if error:
            warning_list.add_error("ERROR: Missing the following field(s): " + error + " on row ID: "+self.id)
        if warning:
            warning_list.add_missing_field("The following field(s) are empty: " + warning + " on row ID: "+self.id)

    def print_fields(self, fieldname):
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
class Composite(Atomic):
    pass
