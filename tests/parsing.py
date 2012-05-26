# -*- coding: utf-8 -*-
import unittest


class RulesTests(unittest.TestCase):
    def setUp(self):
        from fis.parser import Parser
        self.parser = Parser()

    def test_one_variable(self):
        result = self.parser.parse('A = B')
        self.assertEqual(result, 'variables.get_var("A", "B")')

    def test_AND(self):
        result = self.parser.parse('A = B and C = D')
        self.assertEqual(result,
            'variables.get_var("A", "B") & '
            'variables.get_var("C", "D")'
        )

    def test_OR(self):
        result = self.parser.parse('A = B or C = D')
        self.assertEqual(result,
            'variables.get_var("A", "B") | '
            'variables.get_var("C", "D")'
        )

    def test_AND_OR(self):
        result = self.parser.parse('A = B and C = D or E = F')
        self.assertEqual(result,
            'variables.get_var("A", "B") & '
            'variables.get_var("C", "D") | '
            'variables.get_var("E", "F")'
        )

    def test_pharentesis(self):
        result = self.parser.parse('(A = B or C = D) and E = F')
        self.assertEqual(result,
            '(variables.get_var("A", "B") | variables.get_var("C", "D")) & '
            'variables.get_var("E", "F")'
        )

    def test_not(self):
        result = self.parser.parse('not(A = B and C = D)')
        self.assertEqual(result,
            '-(variables.get_var("A", "B") & variables.get_var("C", "D"))'
        )
