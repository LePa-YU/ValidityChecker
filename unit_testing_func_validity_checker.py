import io
import unittest
from unittest.mock import patch
from unittest import TestCase
import func_validity_checker as func

class TestWarningList(TestCase):
    def setUp(self):
        self.warning_list = func.WarningList()

    def test_empty_lists_by_default(self):
        self.assertEqual(self.warning_list.warning, [])
        self.assertEqual(self.warning_list.error, [])
        self.assertEqual(self.warning_list.missing_fields, [])

    def test_add_error(self):
        self.warning_list.add_error("Error: ")
        self.assertEqual(self.warning_list.error, ["Error: "])

    def test_add_warning(self):
        self.warning_list.add_warning("Warning: ")
        self.assertEqual(self.warning_list.warning, ["Warning: "])

    def test_add_missing_field(self):
        self.warning_list.add_missing_field("Field: ")
        self.assertEqual(self.warning_list.missing_fields, ["Field: "])

    def test_print_warning(self):
        self.warning_list.add_warning("Warning: ")
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.warning_list.print_warning()

        self.assertEqual(fake_stdout.getvalue(),"1 Warning: \n")

    def test_print_error(self):
        self.warning_list.add_error("Error: ")
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.warning_list.print_error()

        self.assertEqual(fake_stdout.getvalue(),"1 Error: \n")

    def test_print_missing_fields(self):
        self.warning_list.add_missing_field("Missing fields: ")
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.warning_list.print_missing_fields()

        self.assertEqual(fake_stdout.getvalue(),"1 Missing fields: \n")

    def test_print_msg(self):
        self.warning_list.add_error("Error: ")
        self.warning_list.add_warning("Warning: ")
        self.warning_list.add_missing_field("Missing fields: ")
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.warning_list.print_msg()

        self.assertEqual(fake_stdout.getvalue(), "There are 1 error(s), 1 warning(s), and 1 empty field(s).\n")


class TestHeaderList(TestCase):
    def setUp(self):
        self.header_list = func.Headerlist()
        self.warning_list = func.WarningList()

    def test_empty_lists_by_default(self):
        self.assertEqual(self.header_list.header_modified, [])
        self.assertEqual(self.header_list.header_original, [])

    def test_add_header(self):
        complete_header_list = ['identifier', 'title', 'description', 'url', 'type', 'assesses', 'comesAfter',
                                'alternativeContent', 'requires', 'isPartOf', 'isFormatOf']
        check_header_list = ['identifier', 'title', 'url', 'type', 'assesses', 'comesAfter',
                                'alternativeContent', 'requires', 'isPartOf', 'isFormatOf', 'new_header']
        test_header = ['identifier', 'title', 'url', 'type', 'assesses', 'comesAfter', 'alternativeContent',
                                'requires', 'isPartOf', 'isFormatOf', 'new_header', 'description']
        self.header_list.header_modified = list(map(lambda x: x.lower(),check_header_list))
        self.header_list.add_header(complete_header_list)
        self.assertEqual(self.header_list.header_modified, list(map(lambda x: x.lower(), test_header)))

    def test_check_header_spelling(self):
        warning_list = "1 Warning: Check spelling: assesses\n"
        complete_header_list = ['identifier', 'title', 'description', 'url', 'type', 'assesses', 'comesAfter',
                                'alternativeContent', 'requires', 'isPartOf', 'isFormatOf']
        check_header_list = ['identifier', 'title', 'description', 'url', 'type', 'Assesses', 'comesAfter',
                             'alternativeContent', 'requires', 'isPartOf', 'isFormatOf']
        self.header_list.header_original = check_header_list
        self.header_list.header_modified = list(map(lambda x: x.lower(),check_header_list))

        self.header_list.check_header(warning_list=self.warning_list, real_header=complete_header_list)

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.warning_list.print_warning()

        self.assertEqual(fake_stdout.getvalue(),warning_list)

    def test_check_header_missing_warning(self):
        warning_list = "1 Warning: Missing column(s): description, url, assesses, comesAfter, alternativeContent, requires, isPartOf, isFormatOf\n"
        complete_header_list = ['identifier', 'title', 'description', 'url', 'type', 'assesses', 'comesAfter',
                                'alternativeContent', 'requires', 'isPartOf', 'isFormatOf']
        check_header_list = ['identifier']

        self.header_list.header_original = check_header_list
        self.header_list.header_modified = list(map(lambda x: x.lower(), check_header_list))

        self.header_list.check_header(warning_list=self.warning_list, real_header=complete_header_list)

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.warning_list.print_warning()

        self.assertEqual(fake_stdout.getvalue(), warning_list)

    def test_check_header_missing_error(self):
        warning_list = "1 ERROR: Missing column(s): title, type\n"
        complete_header_list = ['identifier', 'title', 'description', 'url', 'type', 'assesses', 'comesAfter',
                                'alternativeContent', 'requires', 'isPartOf', 'isFormatOf']
        check_header_list = ['identifier']

        self.header_list.header_original = check_header_list
        self.header_list.header_modified = list(map(lambda x: x.lower(), check_header_list))

        self.header_list.check_header(warning_list=self.warning_list, real_header=complete_header_list)

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.warning_list.print_error()

        self.assertEqual(fake_stdout.getvalue(), warning_list)


class TestAtomic(TestCase):
    def setUp(self):
        self.atomic = func.Atomic('', '', '', '', '', '', '', '', '', '', '')
        self.warning_list = func.WarningList()

    def test_confirm_fields_error(self):
        warning_list = "1 ERROR: Missing the following field(s): identifier, title, type on row ID: \n"
        self.atomic.confirm_fields(warning_list=self.warning_list)
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.warning_list.print_error()

        self.assertEqual(fake_stdout.getvalue(), warning_list)

    def test_confirm_fields_print_fields(self):
        warning_list = "1 The following field(s) are empty: description, url, assesses, comesAfter, alternativeContent, requires, isPartOf, isFormatOf on row ID: \n"
        self.atomic.confirm_fields(warning_list=self.warning_list)
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.warning_list.print_missing_fields()

        self.assertEqual(fake_stdout.getvalue(), warning_list)

class TestComposite(TestCase):
    def setUp(self):
        print()