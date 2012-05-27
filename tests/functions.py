# -*- coding: utf-8 -*-

import unittest
from fis.functions import TriangularFunction, Point, TrapezoidalFunction


class TriangularTests(unittest.TestCase):
    def setUp(self):
        # Probamos con el triangulo:
        # (0,0) (20,0) (10,1)
        self.function = TriangularFunction(
            Point(0, 0),
            Point(20, 0),
            Point(10, 1)
        )

    def test_evaluate_equal_to_A(self):
        self.assertEqual(self.function.evaluate(0), 0)

    def test_evaluate_equal_to_B(self):
        self.assertEqual(self.function.evaluate(20), 0)

    def test_evaluate_lower_than_A(self):
        self.assertEqual(self.function.evaluate(-1), 0)

    def test_evaluate_greather_than_B(self):
        self.assertEqual(self.function.evaluate(21), 0)

    def test_evaluate_between_A_C(self):
        self.assertEqual(self.function.evaluate(5), 0.5)

    def test_evaluate_between_C_B(self):
        self.assertEqual(self.function.evaluate(15), 0.5)

    def test_evaluate_in_the_middle(self):
        self.assertEqual(self.function.evaluate(10), 1)

    def test_truncate_middle(self):
        func = self.function.truncate(0.5)
        self.assertIsInstance(func, TrapezoidalFunction)
        self.assertEqual(func.a, self.function.a)
        self.assertEqual(func.b, self.function.b)
        self.assertEqual(func.c, Point(5, 0.5))
        self.assertEqual(func.d, Point(15, 0.5))

    def test_truncate_higher(self):
        func = self.function.truncate(1.1)
        self.assertIsInstance(func, TriangularFunction)
        self.assertEqual(func.a, self.function.a)
        self.assertEqual(func.b, self.function.b)
        self.assertEqual(func.c, self.function.c)

    def test_truncate_zero(self):
        func = self.function.truncate(0)
        self.assertIsInstance(func, TrapezoidalFunction)
        self.assertEqual(func.a, self.function.a)
        self.assertEqual(func.b, self.function.b)
        self.assertEqual(func.c, self.function.a)
        self.assertEqual(func.d, self.function.b)

    def test_truncate_triangle_rectangle(self):
        # Cambiamos los puntos para que sea un triangulo rectangulo
        self.function.b = Point(10, 0)
        self.function.c = Point(10, 1)

        func = self.function.truncate(0.5)
        self.assertIsInstance(func, TrapezoidalFunction)
        self.assertEqual(func.a, self.function.a)
        self.assertEqual(func.b, self.function.b)
        self.assertEqual(func.c, Point(5, 0.5))
        self.assertEqual(func.d, Point(10, 0.5))


class TrapezoidalTests(unittest.TestCase):
    def setUp(self):
        self.function = TrapezoidalFunction(
            Point(0, 0),
            Point(6, 0),
            Point(2, 0.8),
            Point(4, 0.8)
        )

    def test_evaluate_equal_to_A(self):
        self.assertEqual(self.function.evaluate(0), 0)

    def test_evaluate_equal_to_B(self):
        self.assertEqual(self.function.evaluate(6), 0)

    def test_evaluate_lower_than_A(self):
        self.assertEqual(self.function.evaluate(-1), 0)

    def test_evaluate_greather_than_B(self):
        self.assertEqual(self.function.evaluate(21), 0)

    def test_evaluate_between_A_C(self):
        self.assertEqual(self.function.evaluate(1), 0.4)

    def test_evaluate_between_D_B(self):
        self.assertEqual(self.function.evaluate(5), 0.4)

    def test_evaluate_equal_to_C(self):
        self.assertEqual(self.function.evaluate(2), 0.8)

    def test_evaluate_equal_to_D(self):
        self.assertEqual(self.function.evaluate(4), 0.8)

    def test_evaluate_between_C_D(self):
        self.assertEqual(self.function.evaluate(3), 0.8)

    def test_truncate_higher(self):
        func = self.function.truncate(1.1)
        self.assertEqual(func.a, self.function.a)
        self.assertEqual(func.b, self.function.b)
        self.assertEqual(func.c, self.function.c)
        self.assertEqual(func.d, self.function.d)

    def test_truncate_middle(self):
        func = self.function.truncate(0.4)
        self.assertEqual(func.a, self.function.a)
        self.assertEqual(func.b, self.function.b)
        self.assertEqual(func.c, Point(1, 0.4))
        self.assertEqual(func.d, Point(5, 0.4))

    def test_truncate_zero(self):
        func = self.function.truncate(0.4)
        self.assertEqual(func.a, self.function.a)
        self.assertEqual(func.b, self.function.b)
        self.assertEqual(func.c, self.function.c)
        self.assertEqual(func.d, self.function.d)
