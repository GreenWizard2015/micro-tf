import math
import MTF
from MTF.MTFBase import MTFBase
from MTF.MTFGraphNode import MTFGraphNode
from builtins import isinstance

class MTFUnaryOp(MTFBase):
  def __init__(self, L):
    self._X = self._wrap(L)
    return

class MTFSin(MTFUnaryOp):
  def __call__(self, inputs={}):
    X = self._X(inputs)
    if isinstance(X, str):
      return 'sin(%s)' % X
    return math.sin(X)
  
  def d(self):
    return self._X.d() * MTF.cos(self._X)
  
  def simplify(self):
    X = self._X.simplify()
    if X == self._X: return self
    return MTFSin(X)
  
  def graph(self):
    return MTFGraphNode(self, 'sin', self._X)

class MTFCos(MTFUnaryOp):
  def __call__(self, inputs={}):
    X = self._X(inputs)
    if isinstance(X, str):
      return 'cos(%s)' % X
    return math.cos(X)
  
  def d(self):
    return -1 * self._X.d() * MTF.sin(self._X)
  
  def simplify(self):
    X = self._X.simplify()
    if X == self._X: return self
    return MTFCos(X)
  
  def graph(self):
    return MTFGraphNode(self, 'cos', self._X)

class MTFLn(MTFUnaryOp):
  def __call__(self, inputs={}):
    X = self._X(inputs)
    if isinstance(X, str):
      return 'ln(%s)' % X
    
    X = X.real if isinstance(X, complex) else X # is it ok? 
    return math.log(X)
  
  def d(self):
    return self._X.d() * (1.0 / self._X)
  
  def simplify(self):
    X = self._X.simplify()
    if X == self._X: return self
    return MTFLn(X)
  
  def graph(self):
    return MTFGraphNode(self, 'ln', self._X)
  
class MTFExp(MTFUnaryOp):
  def __call__(self, inputs={}):
    X = self._X(inputs)
    if isinstance(X, str):
      return 'exp(%s)' % X
    return math.e ** X
  
  def d(self):
    return self._X.d() * self
  
  def simplify(self):
    X = self._X.simplify()
    if X == self._X: return self
    return MTFExp(X)
  
  def graph(self):
    return MTFGraphNode(self, 'exp', self._X)
  
class MTFNegOp(MTFUnaryOp):
  def __call__(self, inputs={}):
    X = self._X(inputs)
    if isinstance(X, str):
      if ' ' in X: return '(-%s)' % X
      return '-%s' % X
    return -X
  
  def d(self):
    return -self._X.d()
  
  def simplify(self):
    X = self._X.simplify()
    if isinstance(X, MTFNegOp):
      return X._X
    
    if X == self._X: return self
    return MTFNegOp(X)
  
  def graph(self):
    return MTFGraphNode(self, 'negative', self._X)
  
  def value(self):
    return self._X