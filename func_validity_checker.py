
class WarningList:
    def __init__(self):
        self.warning = []
        self.error = []

    def add_error(self, error):
        self.error.append(error)

    def add_warning(self, warning):
        self.warning.append(warning)

    def print_error(self):
        for x in self.error:
            print(x)

    def print_warning(self):
        for x in self.warning:
            print(x)

class Atomic:
    def __init__(self, id, title, alternative, targetUrl, type, assesses, comesAfter, alternativeContent, requires, isRequiredBy, isPartOf, isFormatOf):
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
        if len(self.id) == 0:
            warning_list.add_error("ERROR: Missing ID. ")
        if len(self.title) == 0:
            warning_list.add_error("ERROR: Missing title in "+self.id)
        if len(self.alternative) == 0:
            warning_list.add_warning("Warning: Missing alternative in "+self.id)
        if len(self.targetUrl) == 0:
            warning_list.add_warning("Warning: Missing URL in "+self.id)
        if len(self.type) == 0:
            warning_list.add_error("ERROR: Missing type in "+self.id)
        if len(self.assesses) == 0:
            warning_list.add_warning("Warning: Missing assesses relationships in "+self.id)
        if len(self.comesAfter) == 0:
            warning_list.add_warning("Warning: Missing comesAfter relationships in " + self.id)
        if len(self.alternativeContent) == 0:
            warning_list.add_warning("Warning: Missing alternativeContent relationships in " + self.id)
        if len(self.requires) == 0:
            warning_list.add_warning("Warning: Missing requires relationships in " + self.id)
        if len(self.isRequiredBy) == 0:
            warning_list.add_warning("Warning: Missing isRequiredBy relationships in " + self.id)
        if len(self.isPartOf) == 0:
            warning_list.add_warning("Warning: Missing isPartOf relationships in " + self.id)
        if len(self.isFormatOf) == 0:
            warning_list.add_warning("Warning: Missing isFormatOf relationships in " + self.id)


class Composite(Atomic):
    pass

