# -*- coding: utf-8 -*-

from fis.parser import RuleEvaluator


class FIS(object):
    """
    Representa un sistema de inferencia difusa

    Contiene la siguiente informacion:
    - Variables de entrada
    - Valores iniciales para cada variable de entrada (dictionary)
    - Reglas
    - Variable de salida (se coge automaticamente de la primera regla por el
      momento)

    """
    def FIS(self, input_vars, rules):
        self.input_vars = vars
        self.rules = rules

        #TODO: No funcionara cuando se extienda para N variables de salida
        self.output_var = self.rules[0].output_var

    def execute(self, input_values):
        """
        Metodo principal, encargado de toda la ejecucion del sistema

        """

        evaluator = RuleEvaluator()

        # Evaluamos cada una de las reglas y truncamos
        for rule in self.rules:
            result = evaluator.evaluate(self.input_vars, rule.head)
            rule.output_var.truncate(result)
