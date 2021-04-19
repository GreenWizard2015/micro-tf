from MTF.MTFGraphNode import MTFGraphNode

class MTFBase:
  def __truediv__(self, value):
    import MTF.BinaryOps
    return MTF.BinaryOps.MTFDivOp(self, value)
  
  def __mul__(self, value):
    import MTF.BinaryOps
    return MTF.BinaryOps.MTFMulOp(self, value)
  
  def __add__(self, value):
    import MTF.BinaryOps
    return MTF.BinaryOps.MTFAddOp(self, value)
  
  def __sub__(self, value):
    import MTF.BinaryOps
    return MTF.BinaryOps.MTFSubOp(self, value)
  
  def __pow__(self, value):
    import MTF.BinaryOps
    return MTF.BinaryOps.MTFPowerOp(self, value)

  def __rtruediv__(self, value):
    import MTF.BinaryOps
    return MTF.BinaryOps.MTFDivOp(value, self)
  
  def __rmul__(self, value):
    import MTF.BinaryOps
    return MTF.BinaryOps.MTFMulOp(value, self)

  def __radd__(self, value):
    import MTF.BinaryOps
    return MTF.BinaryOps.MTFAddOp(value, self)
  
  def __rsub__(self, value):
    import MTF.BinaryOps
    return MTF.BinaryOps.MTFSubOp(value, self)
  
  def __rpow__(self, value):
    import MTF.BinaryOps
    return MTF.BinaryOps.MTFPowerOp(value, self)
  
  def __neg__(self):
    import MTF.UnaryOps
    return MTF.UnaryOps.MTFNegOp(self)
  
  def simplify(self):
    raise Exception('Not implemented')
  
  def graph(self):
    raise Exception('Not implemented')
  
  def _wrap(self, value):
    if isinstance(value, MTFBase): return value
    return MTFConstant(value)

class MTFConstant(MTFBase):
  def __init__(self, value):
    self._value = float(value.real if isinstance(value, complex) else value) # is it very bad?
    return
  
  def __call__(self, inputs={}):
    return self._value
  
  def d(self):
    return MTFConstant(0.0)
  
  def graph(self):
    return MTFGraphNode(self, '%.03f' % self._value)
  
  def simplify(self):
    return self