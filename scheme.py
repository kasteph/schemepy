import re

def read(user_input):
  return parser(tokenize(user_input))

def parser(tokens):
  """
  parser(tokenized) -> array (for now)

  Parses the tokens and builds a (nested) array for
  evaluation.

  """
  
  parsed = []

  # So that we can properly recurse
  # and append a nested array
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
  return re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', line.replace('(',' ( ').replace(')',' ) ')  )
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
