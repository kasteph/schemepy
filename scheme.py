import re
import operator

def read(user_input):
  return parser(tokenize(user_input))

def parser(tokens):
  """
  parser(tokenized) -> list (for now)

  Parses the tokens and builds a (nested) list for
  evaluation.

  """
  parsed = []

  open_paren = tokens.pop(0)

  while tokens:

    token = tokens[0]
    if token == '(':
      parsed.append(parser(tokens))
    elif token == ')':
      tokens.pop(0)
      return parsed
    else:
      parsed.append(tokens.pop(0))

  return parsed
    
def tokenize(line):
  """
  tokenize(line) -> string

  Takes a string of Scheme code and breaks it up into
  a series of tokens in a list.
  """
  line = line.replace('(',' ( ').replace(')',' ) ')
  return tokenize_helper(line)

def tokenize_helper(line):
  return transform_nums(preserve_quotes(line))

def preserve_quotes(line):
  regex = r'(?:[^\s,"]|"(?:\\.|[^"])*")+'
  return re.findall(regex, line)
  
def transform_nums(line):
  for index, token in enumerate(line):
    if re.findall(r'\d+.\d+', token):
      line[index] = float(token)
    elif re.findall(r'\d+', token):
      line[index] = int(token)
    else:
      continue
  return line

def is_string(x):
  return isinstance(x, str) and x.startswith('"') and x.endswith('"')

def is_symbol(x):
  return isinstance(x, str) and not is_string(x)

def is_number(x):
  return isinstance(x, (int, float))

def eval(exp, env=None):
  if env == None:
    return eval(exp, Environment([{}]))
  elif is_symbol(exp):
    return env.get(exp)
  elif is_string(exp):
    return exp
  elif is_number(exp):
    return exp
  elif exp[0] == 'quote':
    (_, x) = exp
    return x
  elif exp[0] == 'if':
    (_, test, truthy, falsy) = exp
    return eval((truthy if eval(test) else falsy), env)
  elif exp[0] == 'lambda':
    (_, v, expr) = exp
    new_env = env.create()
    def lambda_func(*args):
      assert len(args) == len(v), 'Something wrong happened'
      new_env.add_scope()
      for param, arg in zip(v, args):
        new_env.set(param, arg)
      return eval(expr, new_env)
    return lambda_func
  # elif is_lambda(exp[0]):
  #   l = exp[0]

  else:
    func = eval(exp[0], env)
    return func(*[eval(x) for x in exp[1:]])


def REP(line):
  return eval(read(line))

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


if __name__ == '__main__':

  while True:
    scheme = raw_input()
    print REP(scheme)
