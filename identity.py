def is_string(x):
  return isinstance(x, str) and x.startswith('"') and x.endswith('"')

def is_symbol(x):
  return isinstance(x, str) and not is_string(x)

def is_number(x):
  return isinstance(x, (int, float))

def is_lambda(x):
  return x[0] == 'lambda'

def is_quote(x):
  return x[0] == 'quote'

def is_if(x):
  return x[0] == 'if'