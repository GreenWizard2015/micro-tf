from collections import namedtuple
from math import factorial
import MTF

def binomialCoef(n):
  nfact = factorial(n)
  return [nfact / (factorial(k) * factorial(n - k)) for k in range(n + 1)]

def generateBinomial(power):
  BinomPart = namedtuple('BinomialPart', ['coef', 'xpower', 'ypower'])
  coefs = binomialCoef(power)
  return [BinomPart(int(coef), xpower=power - k, ypower=k) for k, coef in enumerate(coefs)]
  
################################
x = MTF.Input('x')
y = MTF.Input('y')

power = 5
f = sum(
  B.coef * (x ** B.xpower) * (y ** B.ypower) for B in generateBinomial(power)
).simplify()

f.graph().toGraphViz().render('binom_raw.gv')
f.graph().optimize().toGraphViz().render('binom_optimized.gv')