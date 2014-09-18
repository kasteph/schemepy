import operator

from identity import *
from parser import read

builtins = {
  '+': lambda *args: sum(args),
  '>': operator.gt,
  '<': operator.lt,
  '#t': True,
  '#f': False
}

class Environment(object):
  def __init__(self, scopes):
    self.scopes = scopes
    self.scopes.append(builtins)

  def get(self, symbol):
    for scope in self.scopes:
      if symbol in scope:
        return scope[symbol]

  def set(self, symbol, new_val):
    self.scopes[0][symbol] = new_val

  def add_scope(self):
    self.scopes = [{}] + self.scopes

  def remove_scope(self):
    self.scopes.pop(0)

  def create(self):
    return Environment(self.scopes)

def eval(exp, env=None):
  if env == None:
    return eval(exp, Environment([{}]))
  elif is_symbol(exp):
    return env.get(exp)
  elif is_string(exp):
    return exp
  elif is_number(exp):
    return exp
  elif is_quote(exp):
    (_, x) = exp
    return x
  elif is_if(exp):
    (_, test, truthy, falsy) = exp
    return eval((truthy if eval(test) else falsy), env)
  elif is_let(exp):
    (_, variables, expr) = exp
    (names, vals) = map(lambda L: list(L), list(zip(*variables)))
    exp = ['lambda', names, expr]
    return eval_lambda(exp, env)(*vals)
  elif is_lambda(exp):
    return eval_lambda(exp, env)
  else:
    func = eval(exp[0], env)
    return func(*[eval(x) for x in exp[1:]])

def eval_lambda(exp, env):
  (_, variables, expr) = exp
  new_env = env.create()
  def lambda_func(*args):
    assert len(args) == len(variables), 'Something wrong happened'
    new_env.add_scope()
    for param, arg in zip(variables, args):
      new_env.set(param, arg)
    return eval(expr, new_env)
  return lambda_func

def REP(line):
  return eval(read(line))


if __name__ == '__main__':

  while True:
    scheme = raw_input()
    print REP(scheme)
