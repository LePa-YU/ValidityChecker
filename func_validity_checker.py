import func_helper as helper

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
        print("There are "+str(len(self.error))+" error(s), "+str(len(self.warning))+" warning(s), and " +
              str(len(self.missing_fields))+" empty field(s).")


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

        if 'identifier' not in self.header_modified and 'id' not in self.header_modified:
            error.append('identifier')
            self.header_modified.append('identifier')
        elif 'id' in self.header_modified:
            spelling.append('identifier')


        for header in real_header:
            if (header.lower() not in self.header_modified) and (
                    header.lower() == 'identifier' or header.lower() == 'title' or header.lower() == 'type'):
                error.append(header)
            elif header.lower() not in self.header_modified:
                warning.append(header)
            elif header.strip() not in self.header_original:
                spelling.append(header)

        if error:
            text = helper.print_fields(error)
            warning_list.add_error("ERROR: Missing column(s): "+text)
        if warning:
            text = helper.print_fields(warning)
            warning_list.add_warning("Warning: Missing column(s): "+text)
        if spelling:
            text = helper.print_fields(spelling)
            warning_list.add_warning("Warning: Check spelling: "+text)

class Atomic:
    def __init__(self, identifier, title, description, url, oer_type, assesses, comesAfter, alternativeContent, requires,
                 isPartOf, isFormatOf):
        self.identifier = identifier
        self.title = title
        self.description = description
        self.url = url
        self.oer_type = oer_type
        self.assesses = assesses
        self.comesAfter = comesAfter
        self.alternativeContent = alternativeContent
        self.requires = requires
        self.isPartOf = isPartOf
        self.isFormatOf = isFormatOf

    def confirm_fields(self, warning_list):
        list_error = []
        list_warning = []
        type_warning = []
        if self.identifier is not None:
            if len(self.identifier) == 0:
                list_error.append('identifier')
        if self.title is not None:
            if len(self.title) == 0:
                list_error.append('title')
        if self.oer_type is not None:
            if len(self.oer_type) == 0:
                list_error.append('type')
        if self.description is not None:
            if len(self.description) == 0:
                list_warning.append('description')
        if self.url is not None:
            if len(self.url) == 0:
                list_warning.append('url')
        if self.assesses is not None:
            if len(self.assesses) == 0:
                list_warning.append('assesses')
            elif not self.assesses.isdigit():
                type_warning.append('assesses [type:integer]')
            if len(self.assesses) != 0 and self.oer_type == 'iER':
                type_warning.append('iER should not have an assess property')
        if self.comesAfter is not None:
            if len(self.comesAfter) == 0:
                list_warning.append('comesAfter')
        if self.alternativeContent is not None:
            if len(self.alternativeContent) == 0:
                list_warning.append('alternativeContent')
        if self.requires is not None:
            if len(self.requires) == 0:
                list_warning.append('requires')
        if self.isPartOf is not None:
            if len(self.isPartOf) == 0:
                list_warning.append('isPartOf')
        if self.isFormatOf is not None:
            if len(self.isFormatOf) == 0:
                list_warning.append('isFormatOf')

        error = helper.print_fields(list_error)
        warning = helper.print_fields(list_warning)
        type_warnings = helper.print_fields(type_warning)

        if error:
            warning_list.add_error("ERROR: Missing the following field(s): " + error + " on row ID: "+self.identifier)
        if warning:
            warning_list.add_missing_field("The following field(s) are empty: " + warning + " on row ID: "+self.identifier)
        if type_warnings:
            warning_list.add_error("The following field(s) have an incorrect type: " + type_warnings + " on row ID: "+self.identifier)
class Composite(Atomic):
    pass
