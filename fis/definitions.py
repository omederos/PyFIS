# -*- coding: utf-8 -*-
from copy import copy


class ValueDefinition(object):
    """
    Representa un valor linguistico de una variable

    Guarda la siguiente informacion:
    - Valor linguistico de una cierta variable
    - Funciones de membresia de la variable para ese valor linguistico

    """
    def __init__(self, value, function):
        self.value = value
        self.function = function


class VariableDefinition(object):
    """
    Representa la definicion de una variable

    Contiene la siguiente informacion:
    - Nombre de la variable (ej. Calidad, Propina, etc.)
    - Valor de la variable (ver clase 'Value')

    """
    def __init__(self, name, values=None):
        self.name = name
        if not values:
            values = []
        self.values = values

    def add_value(self, value):
        self.values.append(value)

    def get_value(self, value):
        for v in self.values:
            if v.value == value:
                return v

    def __str__(self):
        return 'Definition: %s %s' % (self.name, self.values)


class Variable(object):
    """
    Representa una variable linguistica (abstracta)

    Contiene la siguiente informacion:
    - Definicion de la variable ('definition')
    - Valor de la variable (ver clase 'Value')

    """
    def __init__(self, definition, value):
        self.definition = definition
        self.value = value

    def __str__(self):
        return '%s = %s' % (self.definition.name, self.value)


class OutputVariable(Variable):
    def __init__(self, definition, value):
        super(OutputVariable, self).__init__(definition, value)

    def truncate(self, value):
        """
        Trunca la funcion de membresia asociada a esta variable

        """
        truncated_function = self.value.function.truncate(value)
        self.value.function = truncated_function


class InputVariable(Variable):
    """
    Esta clase es necesaria pues redefine los operadores &, | y - unario

    Contiene:
    - Todos los campos de 'Variable'
    - Valor inicial
    - Valor obtenido al evaluar la funcion de membresia en el valor inicial
      que tomó esta variable (ej. 0, 1, 0.2, etc.)
    """

    def __init__(self, definition, value, input_value):
        super(InputVariable, self).__init__(definition, value)
        self.input_value = value
        self.membership_value = self.value.function.evaluate(input_value)

    ### Redefinimos los operadores siguientes de acuerdo con la operación
    ### correspondiente en las reglas de la lógica de difusa

    def __and__(self, other):
        d = {self.membership_value: self,
             other.membership_value: other}
        return d[min(self.membership_value, other.membership_value)]

    def __or__(self, other):
        d = {self.membership_value: self,
             other.membership_value: other}
        return d[max(self.membership_value, other.membership_value)]

    def __neg__(self):
        var = copy(self)
        var.membership_value = 1 - self.membership_value
        return var


class VariableCollection(list):
    """
    Representa una lista de definiciones de variables linguisticas

    """
    def __init__(self, seq=()):
        super(VariableCollection, self).__init__(seq)
        self.input = {}

    def get_var(self, variable, value):
        """
        Devuelve la variable linguistica 'variable' con valor ling. 'valor'

        """
        for var in self:
            if var.name == variable:
                return InputVariable(var, var.get_value(value),
                    self.input[var.name])

    def add_input(self, var, value):
        """
        Establece el valor de la variable de entrada 'var' como 'value'

        Ejemplo:
        - Calidad: 3
        - Servicio: 8
        - ...
        """
        self.input[var] = value


class Rule(object):
    def __init__(self, orig_head, head, output_var):
        self.head = head
        self.orig_head = orig_head
        self.output_var = output_var

    def __str__(self):
        return '%s => %s' % (self.orig_head, self.output_var)
