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
        for x in self.error:
            print(x)

    def print_warning(self):
        for x in self.warning:
            print(x)

    def print_missing_fields(self):
        for x in self.missing_fields:
            print(x)


class Headerlist:
    def __init__(self):
        self.header_modified = []
        self.header_original = []

    def add_header(self, real_header):
        for header in real_header:
            if header.lower() not in self.header_modified:
                self.header_modified.append(header.lower())

    def check_header(self, warning_list, real_header):
        for header in real_header:
            if (header.lower() not in self.header_modified) and (
                    header.lower() == 'id' or header.lower() == 'title' or header.lower() == 'type'):
                warning_list.add_error("ERROR: Missing '" + header + "' column.")
            elif header.lower() not in self.header_modified:
                warning_list.add_warning("Warning: Missing '" + header + "' column.")
            elif header not in self.header_original:
                warning_list.add_error("ERROR: check '" + header + "' column spelling.")


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
        if self.alternative is not None:
            if len(self.id) == 0:
                warning_list.add_error("ERROR: Missing ID. ")
        if self.title is not None:
            if len(self.title) == 0:
                warning_list.add_error("ERROR: Missing title in " + self.id)
        if self.type is not None:
            if len(self.type) == 0:
                warning_list.add_error("ERROR: Missing type in " + self.id)

        if self.alternative is not None:
            if len(self.alternative) == 0:
                warning_list.add_missing_field("Missing field: alternative in " + self.id)
        if self.targetUrl is not None:
            if len(self.targetUrl) == 0:
                warning_list.add_missing_field("Missing field: URL in " + self.id)
        if self.assesses is not None:
            if len(self.assesses) == 0:
                warning_list.add_missing_field("Missing field: assesses relationships in " + self.id)
        if self.comesAfter is not None:
            if len(self.comesAfter) == 0:
                warning_list.add_missing_field("Missing field: comesAfter relationships in " + self.id)
        if self.alternativeContent is not None:
            if len(self.alternativeContent) == 0:
                warning_list.add_missing_field("Missing field: alternativeContent relationships in " + self.id)
        if self.requires is not None:
            if len(self.requires) == 0:
                warning_list.add_missing_field("Missing field: requires relationships in " + self.id)
        if self.isRequiredBy is not None:
            if len(self.isRequiredBy) == 0:
                warning_list.add_missing_field("Missing field: isRequiredBy relationships in " + self.id)
        if self.isPartOf is not None:
            if len(self.isPartOf) == 0:
                warning_list.add_missing_field("Missing field: isPartOf relationships in " + self.id)
        if self.isFormatOf is not None:
            if len(self.isFormatOf) == 0:
                warning_list.add_missing_field("Warning: Missing isFormatOf relationships in " + self.id)

class Composite(Atomic):
    pass
