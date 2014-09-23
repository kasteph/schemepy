def is_basestring(x):
  return isinstance(x, basestring)

def is_string(x):
  return is_basestring(x) and x.startswith('"') and x.endswith('"')

def is_symbol(x):
  return is_basestring(x) and not is_string(x)

def is_number(x):
  return isinstance(x, (int, float))

def is_lambda(x):
  return x[0] == 'lambda'

def is_quote(x):
  return x[0] == 'quote'

def is_if(x):
  return x[0] == 'if'

def is_let(x):
  return x[0] == 'let'

def is_define(x):
  return x[0] == 'define'