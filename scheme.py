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


if __name__ == '__main__':

  scheme = raw_input()
  print read(scheme)
