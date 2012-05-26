# -*- coding: utf-8 -*-

import unittest
from fis.functions import TriangularFunction, Point


class TriangularTests(unittest.TestCase):
    def setUp(self):
        # Probamos con el triangulo:
        # (0,0) (20,0) (10,1)
        self.function = TriangularFunction(
            Point(0, 0),
            Point(20, 0),
            Point(10, 1)
        )

    def test_equal_to_A(self):
        self.assertEqual(self.function.evaluate(0), 0)

    def test_equal_to_B(self):
        self.assertEqual(self.function.evaluate(20), 0)

    def test_lower_than_A(self):
        self.assertEqual(self.function.evaluate(-1), 0)

    def test_greather_than_B(self):
        self.assertEqual(self.function.evaluate(21), 0)

    def test_between_A_C(self):
        self.assertEqual(self.function.evaluate(5), 0.5)

    def test_between_C_B(self):
        self.assertEqual(self.function.evaluate(15), 0.5)

    def test_in_the_middle(self):
        self.assertEqual(self.function.evaluate(10), 1)
