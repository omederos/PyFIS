# -*- coding: utf-8 -*-

if __name__ == '__main__':
    from fis.parser import InputParser
    from fis.core import FIS

    f = open('in.txt')
    input_vars, output_var, rules, input_values = InputParser().parse(f)

    fis = FIS(input_vars, output_var, rules)
    fis.execute(input_values)

    print ''
