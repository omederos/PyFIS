# -*- coding: utf-8 -*-
import re


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
