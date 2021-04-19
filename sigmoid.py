import MTF

x = MTF.Input('x')
sigmoid = (1 + MTF.exp(-x)) ** -1

print('Formula: ', sigmoid())
print('Derivative: ', sigmoid.d().simplify()())

print()
print('Alternative')
sigmoid = 1. / (1 + MTF.exp(-x))
print('Formula: ', sigmoid())
print('Derivative: ', sigmoid.d().simplify()())

'''
Output:
Formula:  ((1.0 + exp(-x)) ** -1.0)
Derivative:  (((1.0 + exp(-x)) ** -2.0) * exp(-x)) # same as exp(-x) / ((1.0 + exp(-x)) ** 2.0)

Alternative
Formula:  (1.0 / (1.0 + exp(-x)))
Derivative:  (exp(-x) / ((1.0 + exp(-x)) ** 2.0))

'''