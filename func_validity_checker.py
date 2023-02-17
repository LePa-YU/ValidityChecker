

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
    def __init__(self, ID, title, alternative, targetUrl, type, assesses, comesAfter, alternativeContent, requires, isRequiredBy, isPartOf, isFormatOf):
        self.ID = ID
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
        if len(self.ID) == 0:
            warning_list.add_error("ERROR: Missing ID. ")
        if len(self.title) == 0:
            warning_list.add_error("ERROR: Missing title in "+self.ID)
        if len(self.alternative) == 0:
            warning_list.add_warning("Warning: Missing alternative in "+self.ID)
        if len(self.targetUrl) == 0:
            warning_list.add_warning("Warning: Missing URL in "+self.ID)
        if len(self.type) == 0:
            warning_list.add_error("ERROR: Missing type in "+self.ID)
        if len(self.assesses) == 0:
            warning_list.add_warning("Warning: Missing assesses relationships in "+self.ID)
        if len(self.comesAfter) == 0:
            warning_list.add_warning("Warning: Missing comesAfter relationships in " + self.ID)
        if len(self.alternativeContent) == 0:
            warning_list.add_warning("Warning: Missing alternativeContent relationships in " + self.ID)
        if len(self.requires) == 0:
            warning_list.add_warning("Warning: Missing requires relationships in " + self.ID)
        if len(self.isRequiredBy) == 0:
            warning_list.add_warning("Warning: Missing isRequiredBy relationships in " + self.ID)
        if len(self.isPartOf) == 0:
            warning_list.add_warning("Warning: Missing isPartOf relationships in " + self.ID)
        if len(self.isFormatOf) == 0:
            warning_list.add_warning("Warning: Missing isFormatOf relationships in " + self.ID)

class Composite(Atomic):
    pass

