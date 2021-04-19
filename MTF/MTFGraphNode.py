import graphviz
from _collections import defaultdict
import hashlib

class MTFGraphNode:
  def __init__(self, op, label, *childs):
    self.operation = op
    self.label = label
    self.childs = [
      x if isinstance(x, MTFGraphNode) else x.graph()
      for x in childs
    ]
    self._repr = str(self.operation.simplify()())
    self.hash = hashlib.md5(self._repr.encode()).hexdigest()
    return

  def print(self, level=0):
    print('%s| #%s:%s %s (%s)' % ('  ' * level, self.hash[:8], id(self), self.label, self._repr))
    for x in self.childs:
      x.print(level + 1)
    return
  
  def _collectNodes(self):
    res = [self]
    for x in self.childs:
      res.extend(x._collectNodes())
    return res

  def _reconstruct(self, nodes):
    childs = []
    for x in self.childs:
      if x.hash in nodes:
        node = nodes[x.hash]
      else:
        print('wtf??')
      
      childs.append(node)
    return MTFGraphNode(self.operation, self.label, *childs)
  
  def optimize(self):
    # probably breaks operations execution
    hash2node = {}
    hash2count = defaultdict(int)
    for x in self._collectNodes():
      h = x.hash
      hash2node[h] = x
      hash2count[h] += 1
    
    byDep = [hash2node[x[0]] for x in sorted(hash2count.items(), key=lambda x: x[1], reverse=True)]
    processed = []
    while byDep:
      el = byDep.pop(0)
      if all(x.hash in processed for x in el.childs) or not el.childs:
        hash2count[el.hash] += sum(hash2count[x.hash] for x in el.childs)
        processed.append(el.hash)
      else:
        byDep.append(el)
    #####
    lastNode = None
    for h, n in sorted(hash2count.items(), key=lambda x: x[1], reverse=False):
      hash2node[h] = lastNode = hash2node[h]._reconstruct(hash2node)

    return lastNode
  
  def toGraphViz(self, format='png'):
    res = graphviz.Digraph(format=format)
    nodes = self._collectNodes()
    # create nodes
    for x in nodes:
      res.node('%s_%s' % (x.hash, id(x)), x._repr)
    # create edges
    knownLinks = []
    for x in nodes:
      me = '%s_%s' % (x.hash, id(x))
      for child in x.childs:
        cnode = '%s_%s' % (child.hash, id(child))
        if not ((me + cnode) in knownLinks):
          res.edge(cnode, me)
          knownLinks.append(me + cnode)
    return res
