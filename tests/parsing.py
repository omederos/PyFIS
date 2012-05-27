# -*- coding: utf-8 -*-
import unittest
from fis.definitions import (VariableDefinition, VariableCollection,
                             ValueDefinition)
from fis.functions import TriangularFunction, Point, TrapezoidalFunction
from fis.parser import RuleEvaluator, InputParser


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


class InputParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = InputParser()

    def test_parse_function_triangular(self):
        result = self.parser.parse_function('triangulo: (1,2) (3,4) (5,6)')
        self.assertIsInstance(result, TriangularFunction)
        self.assertEqual(result.a, Point(1, 2))
        self.assertEqual(result.b, Point(3, 4))
        self.assertEqual(result.c, Point(5, 6))

    def test_parse_function_trapezoidal(self):
        result = self.parser.parse_function(
            'trapecio: (1,2) (3,4) (5,6) (7,8)')
        self.assertIsInstance(result, TrapezoidalFunction)
        self.assertEqual(result.a, Point(1, 2))
        self.assertEqual(result.b, Point(3, 4))
        self.assertEqual(result.c, Point(5, 6))
        self.assertEqual(result.d, Point(7, 8))

    def test_parse_input_vars(self):
        result = self.parser.parse_input_vars(
            """
            input: (Calidad) (Buena) (triangulo: (1,2) (3,4) (5,6))
            input: (Calidad) (Regular) (trapecio: (1,2) (3,4) (5,6) (7,8))
            input: (Calidad) (Mala) (trapecio: (1,2) (3,4) (5,6) (7,8))

            input: (Comida) (Buena) (triangulo: (1,2) (3,4) (5,6))
            input: (Comida) (Regular) (trapecio: (1,2) (3,4) (5,6) (7,8))
            input: (Comida) (Mala) (trapecio: (1,2) (3,4) (5,6) (7,8))
            """
        )
        self.assertIsInstance(result, VariableCollection)
        self.assertEqual(len(result), 2)

        calidad = result[0]

        self.assertEqual(len(calidad.values), 3)
        self.assertEqual(calidad.values[0].value, 'Buena')
        self.assertIsInstance(calidad.values[0].function, TriangularFunction)
        self.assertEqual(calidad.values[1].value, 'Regular')
        self.assertIsInstance(calidad.values[1].function, TrapezoidalFunction)
        self.assertEqual(calidad.values[2].value, 'Mala')
        self.assertIsInstance(calidad.values[2].function, TrapezoidalFunction)

        comida = result[1]
        self.assertEqual(len(comida.values), 3)
        self.assertEqual(comida.values[0].value, 'Buena')
        self.assertIsInstance(comida.values[0].function, TriangularFunction)
        self.assertEqual(comida.values[1].value, 'Regular')
        self.assertIsInstance(comida.values[1].function, TrapezoidalFunction)
        self.assertEqual(comida.values[2].value, 'Mala')
        self.assertIsInstance(comida.values[2].function, TrapezoidalFunction)

    def test_parse_output_var(self):
        calidad = self.parser.parse_output_var(
            """
            output: (Calidad) (Buena) (triangulo: (1,2) (3,4) (5,6))
            output: (Calidad) (Regular) (trapecio: (1,2) (3,4) (5,6) (7,8))
            """
        )
        self.assertIsInstance(calidad, VariableDefinition)

        self.assertEqual(len(calidad.values), 2)
        self.assertEqual(calidad.values[0].value, 'Buena')
        self.assertIsInstance(calidad.values[0].function, TriangularFunction)
        self.assertEqual(calidad.values[1].value, 'Regular')
        self.assertIsInstance(calidad.values[1].function, TrapezoidalFunction)

    def test_parse_rules(self):
        text = """
        output: (Calidad) (Buena) (triangulo: (1,2) (3,4) (5,6))
        output: (Calidad) (Regular) (trapecio: (1,2) (3,4) (5,6) (7,8))

        rule: VarA = ValueA => Buena
        rule: not(VarA = ValueA) => Buena
        rule: VarA = ValueA and VarB = ValueB => Regular
        rule: VarA = ValueA or VarB = ValueB => Regular
        rule: (VarA = ValueA or VarB = ValueB) and ValueB = VarA => Buena
        rule: not(VarA = ValueA or VarB = ValueB) => Regular
        """
        output_var_def = self.parser.parse_output_var(text)

        rules = self.parser.parse_rules(text, output_var_def)
        self.assertEqual(len(rules), 6)

        self.assertEqual(rules[0].orig_head, 'VarA = ValueA')
        # Asegurarnos de que se parsea la regla
        self.assertEqual(rules[0].head,
            'variables.get_var("VarA", "ValueA")')
        self.assertEqual(rules[0].output_var.definition, output_var_def)
        self.assertEqual(rules[0].output_var.value.value, 'Buena')

        #...

        self.assertEqual(rules[5].output_var.value.value, 'Regular')

    def test_parse_input_values(self):
        text = """
            ini: Calidad = 13
            ini: Temperatura = 10
            ini: Propina = 16.3
            """
        d = self.parser.parse_input_values(text)
        self.assertEqual(len(d), 3)
        self.assertEqual(d['Calidad'], 13)
        self.assertEqual(d['Temperatura'], 10)
        self.assertEqual(d['Propina'], 16.3)
