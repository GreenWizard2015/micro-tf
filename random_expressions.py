import random
from MTF.UnaryOps import *
from MTF.BinaryOps import *
import MTF

ops = {
  'unary': [MTFSin, MTFCos, MTFLn, MTFExp, MTFNegOp],
  'binary': [MTFAddOp, MTFSubOp, MTFMulOp, MTFDivOp, MTFPowerOp]
}

def createF(inputs, complexity):
  opsN = 0
  freeNodes = [*inputs]
  for _ in range(complexity):
    freeNodes.append(MTFConstant(int(100 * (random.random() * 2. - 1.)) / 10.0 ))
    
  while (1 < len(freeNodes)):
    binaryOp = (random.random() < .85) and (1 < len(freeNodes))
    opsSet = ops['binary' if binaryOp else 'unary']
    argsSet = freeNodes + inputs if opsN < complexity else freeNodes

    args = [random.choice(argsSet)]
    if binaryOp:
      args.append(random.choice(argsSet))

    for x in args:
      if x in freeNodes: freeNodes.remove(x)
    
    freeNodes.append(random.choice(opsSet)(*args))
    opsN += 1
  return freeNodes[0]

x = MTF.Input('x')
y = MTF.Input('y')

for n in range(100):
  try:
    f = createF([x, y], complexity=50)
    print(f.simplify()())
  except:
    pass # ignore invalid expressions