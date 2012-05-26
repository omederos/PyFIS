# -*- coding: utf-8 -*-


class Point(object):
    """
    Representa un punto en 2D

    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TriangularFunction(object):
    """
    Representa una funcion de membresia triangular

    Los puntos deben ser especificados de la siguiente forma:
    'a': punto sobre el eje X mas a la izquierda
    'b: punto sobre el eje X mas a la derecha
    'c': tercer punto del triangulo (el que define su altura)

    """
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def evaluate(self, value):
        """
        Devuelve un valor en el intervalo [0,1] que indica la membresia

        """

        # Si valor esta fuera del triangulo
        if value <= self.a.x or value >= self.b.x:
            return 0

        # Usamos float para que la division no sea en enteros
        value = float(value)

        # Si el valor caerá en la recta 'ac'
        if self.a.x < value <= self.c.x:
            return (value - self.a.x) / (self.c.x - self.a.x) * self.c.y

        # Si el valor caerá en la recta 'cb'
        return (self.b.x - value) / (self.b.x - self.c.x) * self.c.y
