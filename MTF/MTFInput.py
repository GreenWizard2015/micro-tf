from MTF.MTFGraphNode import MTFGraphNode
from MTF.MTFBase import MTFBase

class MTFInput(MTFBase):
  def __init__(self, name):
    self._name = name
    return
  
  def __call__(self, inputs={}):
    return inputs[self] if self in inputs else self._name
  
  def d(self):
    return 1
  
  def graph(self):
    return MTFGraphNode(self, self._name)
  
  def simplify(self):
    return self