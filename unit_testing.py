import unittest
from unittest import mock
from unittest import TestCase
import func_validity_checker
import validity_checker

class TestOutput(unittest.TestCase):
    @mock.patch('validity_checker.input', create=True)
    def testDictionary(self, mocked_input):
        mocked_input.side_effect = ['C:\Users\Anni\working_environment\ValidityChecker\Datasets\FAKE1001.csv', 'e', 'w', 'f']
        result = dictCreate(1)
        self.assertEqual(result, {})

    print()