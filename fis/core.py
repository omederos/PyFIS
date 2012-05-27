# -*- coding: utf-8 -*-
from fis.definitions import VariableCollection

from fis.parser import RuleEvaluator


class FIS(object):
    """
    Representa un sistema de inferencia difusa

    Contiene la siguiente informacion:
    - Variables de entrada (VariableCollection)
    - Valores iniciales para cada variable de entrada (dictionary)
    - Variable de salida (VariableDefinition)
    - Reglas

    """
    def FIS(self, input_vars, output_var, rules):
        self.input_vars = input_vars
        self.rules = rules
        self.output_var = output_var

    def execute(self, input_values):
        """
        Metodo principal, encargado de toda la ejecucion del sistema

        """
        evaluator = RuleEvaluator()

        # Guardamos los valores iniciales que toman las variables de entrada
        for var, value in input_values.items():
            self.input_vars.add_input(var, value)

        # Evaluamos cada una de las reglas y truncamos c/ funcion
        for rule in self.rules:
            result = evaluator.evaluate(self.input_vars, rule.head)
            rule.output_var.truncate(result)
