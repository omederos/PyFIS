# -*- coding: utf-8 -*-


class Point(object):
    """
    Representa un punto en 2D

    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%s,%s)" % (self.x, self.y)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return other.x == self.x and other.y == self.y


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

        # Si el valor esta fuera del triangulo
        if value <= self.a.x or value >= self.b.x:
            return 0

        # Usamos float para que la division no sea en enteros
        value = float(value)

        # Si el valor caerá en la recta 'ac'
        if self.a.x < value <= self.c.x:
            return (value - self.a.x) / (self.c.x - self.a.x) * self.c.y

        # Si el valor caerá en la recta 'cb'
        return (self.b.x - value) / (self.b.x - self.c.x) * self.c.y

    def truncate(self, value):
        """
        Trunca la funcion (superiormente) por el valor especificado

        Si la funcion es finalmente truncada, se convertira en una funcion
        trapezoidal

        Debe retornar la funcion resultante
        """

        # Si el valor esta por encima del triangulo
        if value > self.c.y:
            return self

        if not value:
            c = self.a
            d = self.b
        else:
            value = float(value)
            c = Point(
                value * (self.c.x - self.a.x) / self.c.y + self.a.x,
                value
            )
            d = Point(
                value * (self.b.x - self.c.x) / self.c.y + self.c.x,
                value
            )

        trapezoidal_function = TrapezoidalFunction(self.a, self.b, c, d)
        return trapezoidal_function

    def __str__(self):
        return "Triangular Function: %s %s %s" % self.a, self.b, self.c


class TrapezoidalFunction(object):
    """
    Representa una funcion de membresia trapezoidal

    Los puntos deben ser especificados de la siguiente forma:
    'a': punto sobre el eje X mas a la izquierda
    'b: punto sobre el eje X mas a la derecha
    'c': punto que no esta sobre el eje X (mas a la izquierda)
    'd': punto que no esta sobre el eje X (mas a la derecha)

    """
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def evaluate(self, value):
        # Si el valor esta fuera del trapecio
        if value <= self.a.x or value >= self.b.x:
            return 0

        # Usamos float para que la division no sea en enteros
        value = float(value)

        # Si el valor caerá en la recta 'ac'
        if self.a.x < value < self.c.x:
            return TriangularFunction(
                self.a,
                Point(self.c.x, 0),
                self.c
            ).evaluate(value)

        # Si el valor cae en la recta paralela al eje X
        if self.c.x <= value <= self.d.x:
            return self.c.y

        # Sino, el valor caerá en la recta 'cb'
        return TriangularFunction(
            Point(self.d.x, 0),
            self.b,
            self.d
        ).evaluate(value)

    def __str__(self):
        return "Trapezoidal Function: %s %s %s %s" % (self.a, self.b, self.c,
                                                      self.d)

    def truncate(self, value):
        """
        Trunca la funcion (superiormente) por el valor especificado

        Genera los nuevos puntos basandose en la function 'truncate' del
        triangulo, truncando los dos triangulos de las esquinas del trapecio
        (DRY)

        Retorna la funcion resultante con los puntos del trapecio modificados
        """

        # Si el valor esta por encima del triangulo o es cero
        if value > self.c.y or value == 0:
            return self

        # Truncar el triangulo de la izquierda y coger el pto que nos interesa
        f1 = TriangularFunction(self.a, Point(self.c.x, 0), self.c)
        trap1 = f1.truncate(value)
        self.c = trap1.c

        # Truncar el triangulo de la derecha y coger el pto que nos interesa
        f2 = TriangularFunction(Point(self.d.x, 0), self.b, self.d)
        trap2 = f2.truncate(value)

        self.d = trap2.d

        return self
