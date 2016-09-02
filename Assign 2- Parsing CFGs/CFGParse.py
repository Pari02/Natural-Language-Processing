import sys, re, codecs


class PSG:
  """This is a storage and parser class for context free grammars
written in the format of reproduction or replacement rules.
  """

  # symbol: [^-=>#,\s]+([-]+[^-=>#,\s]+)*
  rule_re = re.compile(r"(?P<lhssymbol>[^-=>#,\s]+([-]+[^-=>#,\s]+)*)\s+(-+|=+)>\s+(?P<rhssymbols>[^-=>#,\s]+([-]+[^-=>#,\s]+)*(\s+[^-=>#,\s]+([-]+[^-=>#,\s]+)*)*)(\s*#.*)?")

  def __init__(self, filename):
    self.terminals    = set()  # list of terminals
    self.nonterminals = set()  # list of non-terminals
    self.id2symb      = {}
    self.symb2id      = {}
    self.lhshash      = {}
    self.rhshash      = {}
    self.load(filename)

  def load(self, filename):
    rules = {}
    fp = codecs.open(filename, 'r', 'utf-8')
    line = fp.readline()
    while line:
      line = line.strip()
      res = self.rule_re.match(line)
      if res:
        lhs = res.group('lhssymbol')
        rhs = tuple(res.group('rhssymbols').split())
        ruletuple = (lhs, rhs)
        rules[ruletuple] = rules.get(ruletuple, 0) + 1
      line = fp.readline()
    fp.close()

    # make sets of terminals and non-terminals
    symbcount = 0
    for rule in rules:
      lhs = rule[0]
      rhs = rule[1]
      if lhs not in self.symb2id:
        symbcount += 1
        self.symb2id[lhs] = symbcount
      lhs = self.symb2id[lhs]
      self.nonterminals.add(lhs)
      nrhs = []
      for symb in rhs:
        if symb not in self.symb2id:
          symbcount += 1
          self.symb2id[symb] = symbcount
        nrhs.append(self.symb2id[symb])
      rhs = tuple(nrhs)
      # make lhs mapping to rhs
      res = list(self.lhshash.get(lhs, ()))
      if rhs not in res:
        res.append(rhs)
        self.lhshash[lhs] = tuple(res)
      # make rule for left-peripheral rhs symbol as key
      res = list(self.rhshash.get(rhs[0], ()))
      rule = (lhs, rhs)
      if rule not in res:
        res.append(rule)
        self.rhshash[rhs[0]] = tuple(res)
      # 
    self.id2symb = dict([ (t[1], t[0]) for t in self.symb2id.items() ])
    self.terminals = set(self.id2symb.keys()).difference(self.nonterminals)

  def id2s(self, id):
    return self.id2symb.get(id, "")

  def idl2s(self, idlist):
    return tuple( ( self.id2symb.get(i, "") for i in idlist ) )

  def s2id(self, symb):
    return self.symb2id.get(symb, 0)

  def sl2id(self, symblist):
    return tuple( ( self.symb2id.get(symb, 0) for symb in symblist ) )

  def isTerminal(self, id):
    if id in self.terminals: return True
    return False

  def isSymbol(self, id):
    if id in self.nonterminals: return True
    return False
