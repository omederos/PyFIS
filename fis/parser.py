# -*- coding: utf-8 -*-
import re
from fis.definitions import (VariableCollection, VariableDefinition,
                             ValueDefinition)
from fis.functions import Point, TriangularFunction, TrapezoidalFunction


class RuleEvaluator(object):
    """
    Clase encargada de evaluar el encabezado de una regla

    """
    def __init__(self):
        self.parser = RuleParser()

    def evaluate(self, variables, rule_head):
        """
        Evalua el encabezado de la regla dada

        El parametro 'variables' es utilizado en el codigo que se evaluará
        utilizando la función 'eval'
        """
        parsed = self.parser.parse(rule_head)
        var = eval(parsed)
        return var.membership_value


class RuleParser(object):
    """
    Parsea una regla y la convierte a código Python lista para evaluarse

    """
    def _replace(self, match):
        """
        Funcion que reemplaza el texto 'Variable = Valor'

        Lo reemplaza por el codigo correspondiente en Python que se ejecutara
        posteriormente

        """
        return 'variables.get_var("%s", "%s")' % (match.group(1),
                                                  match.group(2))

    def parse(self, head):
        """
        Parsea un encabezado y lo convierte a codigo Python
        """
        head = head.replace(' and ', ' & ').replace(' or ', ' | ')
        head = head.replace('not(', '-(')
        pattern = re.compile('([A-Z]\w*)\s+=\s+([A-Z]\w*)')
        return pattern.sub(self._replace, head)


class InputParser(object):
    """
    Parsea un texto o fichero de entrada

    El texto debe tener el siguiente formato:

    # Varias variables de entrada
    input: (Var1) (Value1) (triangulo/trapecio: (x,y) (x,y) ...)
    input: (Var1) (Value2) (triangulo/trapecio: (x,y) (x,y) ...)
    input: (Var1) (Value3) (triangulo/trapecio: (x,y) (x,y) ...)
    ...
    input: (Var2) (Value1) (triangulo/trapecio: (x,y) (x,y) ...)
    input: (Var2) (Value2) (triangulo/trapecio: (x,y) (x,y) ...)
    input: (Var3) (Value3) (triangulo/trapecio: (x,y) (x,y) ...)

    # Una sola variable de salida (Var1)
    output: (output_Var) (output_Value1) (triangulo/trapecio: (x,y) (x,y) ...)
    output: (output_Var) (output_Value3) (triangulo/trapecio: (x,y) (x,y) ...)
    output: (output_Var) (output_Value1) (triangulo/trapecio: (x,y) (x,y) ...)

    # Reglas. Ejemplos de reglas:
    rule: Var1 = Value1 => output_Value1
    rule: not(Var1 = Value1) => output_Value2
    rule: Var1 = Value1 and Var2 = Value2 => output_Value3
    rule: Var1 = Value1 or Var2 = Value2 => output_Value1
    rule: (Var1 = Value1 or Var2 = Value2) and Value2 = Var1 => output_Value3
    rule: not(Var1 = Value1 or Var2 = Value2) => output_Value2
    ...

    # Valores iniciales de las variables:
    ini: Var1 = 10
    ini: Var2 = 20
    ...

    """
    def parse(self, text):
        # Si es un fichero, leemos su contenido
        if hasattr(text, 'read'):
            text = text.read()

        # Parseando las variables de entrada
        input_vars = self.parse_input_vars(text)

        # Parseando la variable de salida
        output_var = self.parse_output_var(text)

    def parse_input_vars(self, text):
        pattern = re.compile(r'input: \((\w+)\) \((\w+)\) \((.*)\)')
        m = pattern.search(text)

        d = {}

        while m:
            name = m.group(1)
            value_raw = m.group(2)
            func = self.parse_function(m.group(3))

            value = ValueDefinition(value_raw, func)
            if not name in d:
                d[name] = []

            d[name].append(value)

            m = pattern.search(text, m.end())

        variables = VariableCollection()

        for name, values in d.items():
            variables.append(VariableDefinition(name, values))

        return variables

    def parse_function(self, text):
        m = re.match('(triangulo|trapecio): (.*)', text)
        if not m:
            raise Exception('Error parseando la funcion: %s' % text)

        func_type = m.group(1)
        points_raw = m.group(2)

        points = []

        pattern = re.compile(r'\(([\d\.]+),\s*([\d\.]+)\)')
        m = pattern.search(points_raw)

        while m:
            points.append(Point(float(m.group(1)), float(m.group(2))))
            m = pattern.search(points_raw, m.end())

        if func_type == 'triangulo':
            cls = TriangularFunction
        else:
            cls = TrapezoidalFunction
        return cls(*points)

    def parse_output_var(self, text):
        pattern = re.compile(r'output: \((\w+)\) \((\w+)\) \((.*)\)')
        m = pattern.search(text)

        d = {}

        while m:
            name = m.group(1)
            value_raw = m.group(2)
            func = self.parse_function(m.group(3))

            value = ValueDefinition(value_raw, func)
            if not name in d:
                d[name] = []

            d[name].append(value)

            m = pattern.search(text, m.end())

        name = d.items()[0][0]
        values = d.items()[0][1]

        return VariableDefinition(name, values)
