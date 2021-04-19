from .MTFBase import MTFBase, MTFConstant
from .MTFGraphNode import MTFGraphNode
import MTF
from builtins import isinstance
from MTF.UnaryOps import MTFNegOp

class MTFBinOp(MTFBase):
  def __init__(self, L, R):
    self._L = self._wrap(L)
    self._R = self._wrap(R)
    return
  
  def __call__(self, inputs={}):
    L = self._L(inputs)
    R = self._R(inputs)
    if any(isinstance(x, str) for x in (L, R)):
      return '(%s %s %s)' % (str(L), self.OP_SYMBOL, str(R))
    return self.OP(L, R)
  
  def simplify(self):
    L = self._L.simplify()
    R = self._R.simplify()
    unchanged = (L == self._L) and (R == self._R)
    return self._simplify(L, R, not unchanged)
  
  def graph(self):
    return MTFGraphNode(self, self.OP_SYMBOL, self._L, self._R)
  
class MTFAddOp(MTFBinOp):
  OP_SYMBOL = '+'
  OP = lambda _, a, b: a + b
  
  def __init__(self, L, R):
    L = self._wrap(L)
    R = self._wrap(R)
    args = list(sorted((L, R), key=lambda x: str(x())))
    return super().__init__(*args)
  
  def d(self):
    return self._L.d() + self._R.d()
  
  def _simplify(self, L, R, changed):
    LVal = L()
    RVal = R()
    if all(isinstance(x, MTFConstant) for x in (L, R)):
      return MTFConstant(LVal + RVal)
    
    if RVal == LVal: return 2 * R
    if LVal == 0: return R
    if RVal == 0: return L
    
    return self._wrap(L + R) if changed else self
  
class MTFSubOp(MTFBinOp):
  OP_SYMBOL = '-'
  OP = lambda _, a, b: a - b
  
  def d(self):
    return self._L.d() - self._R.d()

  def _simplify(self, L, R, changed):
    LVal = L()
    RVal = R()
    if all(isinstance(x, MTFConstant) for x in (L, R)):
      return MTFConstant(LVal - RVal)
    
    if RVal == LVal: return MTFConstant(0)
    if RVal == 0: return L
    if LVal == 0: return (-R).simplify()
    
    return self._wrap(L - R) if changed else self
  
class MTFMulOp(MTFBinOp):
  OP_SYMBOL = '*'
  OP = lambda _, a, b: a * b
  
  def __init__(self, L, R):
    L = self._wrap(L)
    R = self._wrap(R)
    args = list(sorted((L, R), key=lambda x: str(x())))
    return super().__init__(*args)
  
  def d(self):
    return (self._L * self._R.d()) + (self._R * self._L.d())
  
  def _simplify(self, L, R, changed):
    LVal = L()
    RVal = R()
    if all(isinstance(x, MTFConstant) for x in (L, R)):
      return MTFConstant(LVal * RVal)
    
    if RVal == 1: return L  
    if LVal == 1: return R
    
    if RVal == -1: return (-L).simplify()
    if LVal == -1: return (-R).simplify()
    if (RVal == 0) or (LVal == 0): return MTFConstant(0)
    
    if RVal == LVal: return L ** 2
    if any(isinstance(x, MTFPowerOp) for x in (L, R)):
      baseL = L.base() if isinstance(L, MTFPowerOp) else LVal
      baseR = R.base() if isinstance(R, MTFPowerOp) else RVal
      if baseL == baseR:
        powerL = L.power if isinstance(L, MTFPowerOp) else 1
        powerR = R.power if isinstance(R, MTFPowerOp) else 1
        base = L.base if isinstance(L, MTFPowerOp) else R.base
        res = base ** (powerL + powerR)
        return res.simplify()
      
    
    if all(isinstance(x, MTFNegOp) for x in (L, R)):
      return L.value() * R.value()

    return self._wrap(L * R) if changed else self
  
class MTFDivOp(MTFBinOp):
  OP_SYMBOL = '/'
  OP = lambda _, a, b: a / b
  
  def d(self):
    f = self._L
    g = self._R
    return ((f.d() * g) - (f * g.d())) / (g ** 2)
  
  def _simplify(self, L, R, changed):
    LVal = L()
    RVal = R()
    if all(isinstance(x, MTFConstant) for x in (L, R)):
      return MTFConstant(LVal / RVal)
    
    if LVal == RVal: return MTFConstant(0) # x / x = 1
    if LVal == 0: return MTFConstant(0) # 0 / x = 0
    if RVal == 1: return L # x / 1 = x
    
    return self._wrap(L / R) if changed else self
  
class MTFPowerOp(MTFBinOp):
  OP_SYMBOL = '**'
  OP = lambda _, a, b: a ** b
  
  def __init__(self, L, R):
    super().__init__(L, R)
    self.base = self._L
    self.power = self._R
    return

  def d(self):
    lval = self._L()
    if not isinstance(lval, str): # base is a constant
      return (lval ** self._R) * self._R.d() * MTF.ln(lval)
    
    # d(u ** v) = v * (u ** (v - 1)) * d(u)
    return self._R * (self._L ** (self._R - 1)) * self._L.d()
  
  def _simplify(self, L, R, changed):
    LVal = L()
    RVal = R()
    if all(isinstance(x, MTFConstant) for x in (L, R)):
      return MTFConstant(LVal ** RVal)
    
    if LVal == 1: return MTFConstant(1) # 1 ** x = 1
    if RVal == 0: return MTFConstant(1) # x ** 0 = 1
    if RVal == 1: return L # x ** 1 = x
    if LVal == 0: return MTFConstant(0) # 0 ** x = 0
    
    return self._wrap(L ** R) if changed else self
  
  def graph(self):
    power = self.power()
    if not isinstance(power, str):
      if 0 == power: return MTFConstant(1)
      if power == int(power):
        expanded = self.base
        for _ in range(int(abs(power - 1))):
          expanded *= self.base
        
        if power < 0:
          expanded = 1 / expanded
        
      return expanded.graph()
    return MTFGraphNode(self, self.OP_SYMBOL, self._L, self._R)
