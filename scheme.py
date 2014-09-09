def parenthesize(line):
  if line.find('(') >= 0:
    line = line.replace('(', ' ( ', len(line))

  if line.find(')') >= 0:
    line = line.replace(')', ' ) ', len(line))

  return line

def tokenize(line):
  """
  tokenize(line) -> string

  Takes a string of Scheme code and breaks it up into
  a series of tokens.
  """

  line = parenthesize(line)

  line = line.split(' ')
  return line