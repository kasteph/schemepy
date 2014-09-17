import re

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


# isa and Symbol from Norvig's lis.py
isa = isinstance
Symbol = str
Number = (int, float)
quotes = '"'
def eval(exp, env=None):
  current_exp = exp[0]
  if env == None:
    return eval(exp, Environment([{}]))
  # elif isa(exp, Symbol):
  #   return exp
  # elif isa(exp, Number):
  #   return exp
  # elif isa(current_exp, str) and quotes in exp:
  #   return env.get(current_exp)
  # elif isa(exp, str) and quotes not in exp:
  #   return env.get(exp)
  # elif exp[0]



class Environment(object):
  def __init__(self, scopes):
    self.scopes = scopes

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



if __name__ == '__main__':

  scheme = raw_input()
  print read(scheme)
