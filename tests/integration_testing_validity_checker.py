import io
import unittest
from unittest import TestCase
from unittest.mock import patch
import func_helper as helper
import func_validity_checker as func
# import pytest

class IntegrationTest(TestCase):
    def setUp(self):
        self.complete_header_list = ['identifier', 'title', 'description', 'url', 'type', 'assesses', 'comesAfter',
                                     'alternativeContent', 'requires', 'isPartOf', 'isFormatOf']
        self.warning_list = func.WarningList()
        self.header_list = func.Headerlist()
        self.file_path_fake = "/Test_Datasets/FAKE1001.csv"

    def test_empty_lists_by_default(self):
        self.assertEqual(self.warning_list.warning, [])
        self.assertEqual(self.warning_list.error, [])
        self.assertEqual(self.warning_list.missing_fields, [])

    def TestOpenFile(self):
        helper.open_file(self.warning_list, self.header_list, self.complete_header_list,
                                            self.file_path_fake)

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.warning_list.print_warning()

        self.assertEqual(fake_stdout.getvalue(), "1 Error: \n")

        # self.assertEqual(self.warning_list.print_warning(), "")
        # self.assertEqual(self.warning_list.print_error(), "")
        # self.assertEqual(self.warning_list.print_missing_fields(), "")


if __name__ == '__main__':
    unittest.main()





