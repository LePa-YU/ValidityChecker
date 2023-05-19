import unittest
from unittest import mock
from unittest import TestCase
import func_helper as helper


# func_helper
class TestCheckDict(TestCase):
    def test_check_dict(self):
        actual = helper.check_dict(file_dict=, warning_list=)
        expected = {}
        self.assertEqual(actual, expected)

class TestConfirmRelationships(TestCase):
    def test_confirm_relationships(self):
        actual = helper.confirm_relationships(key=,er=,warning_list=)
        expected = {}
        self.assertEqual(actual, expected)

class TestConfirmDisconnectedNode(TestCase):
    def test_confirm_disconnected_node(self):
        actual = helper.confirm_disconnected_node(file_dict=, key=, er=, warning_list=)
        expected = {}
        self.assertEqual(actual, expected)

class TestConfirmStartEndNodes(TestCase):
    def test_confirm_start_end_nodes(self):
        actual = helper.confirm_disconnected_node(key=, er=, warning_list=, node=, type=)
        expected = {}
        self.assertEqual(actual, expected)

class TestCheckIfFieldExists(TestCase):
    def test_check_if_field_exists(self):
        actual = helper.check_if_field_exists(er=, er_list=, list_comesAfter=)
        expected = {}
        self.assertEqual(actual, expected)

class TestCheckIfFieldExists(TestCase):
    def test_print_fields(self):
        actual = helper.print_fields(fieldname=)
        expected = {}
        self.assertEqual(actual, expected)
