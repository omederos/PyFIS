# -*- coding: utf-8 -*-
import unittest
from fis.definitions import (VariableDefinition, VariableCollection,
                             ValueDefinition)
from fis.functions import TriangularFunction, Point
from fis.parser import RuleEvaluator


class ParserTests(unittest.TestCase):
    def setUp(self):
        from fis.parser import RuleParser
        self.parser = RuleParser()

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


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        f1 = TriangularFunction(
            Point(0, 0),
            Point(10, 0),
            Point(5, 1)
        )
        f2 = TriangularFunction(
            Point(5, 0),
            Point(15, 0),
            Point(10, 1)
        )

        agua_values = [
            ValueDefinition('Fria', f1),
            ValueDefinition('Tibia', f2)
        ]

        propina_values = [
            ValueDefinition('Poca', f1),
            ValueDefinition('Mucha', f2)
        ]

        self.variables = VariableCollection(
            (
                VariableDefinition('Agua', agua_values),
                VariableDefinition('Propina', propina_values)
                )
        )
        self.variables.add_input('Agua', 2.5)
        self.variables.add_input('Propina', 7.5)

        self.evaluator = RuleEvaluator()

    def test_one_var(self):
        result = self.evaluator.evaluate(self.variables, 'Agua = Fria')
        self.assertEqual(result, 0.5)

    def test_one_var_(self):
        result = self.evaluator.evaluate(self.variables, 'Agua = Tibia')
        self.assertEqual(result, 0)

    def test_OR(self):
        result = self.evaluator.evaluate(self.variables,
            'Agua = Fria or Agua = Tibia')
        self.assertEqual(result, 0.5)

    def test_AND(self):
        result = self.evaluator.evaluate(self.variables,
            'Agua = Fria and Agua = Tibia')
        self.assertEqual(result, 0)

    def test_NOT(self):
        result = self.evaluator.evaluate(self.variables,
            'not(Agua = Tibia)')
        self.assertEqual(result, 1)
