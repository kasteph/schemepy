def tokenize(line):
  """
  tokenize(line) -> string

  Takes a string of Scheme code and breaks it up into
  a series of tokens.
  """

  line = line.replace('(', ' ( ').replace(')', ' ) ').split(' ')
  return [atom for atom in line if atom]

if __name__ == '__main__':

  print tokenize('((lambda(x) x "Lisp")')