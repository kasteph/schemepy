import operator

builtins = {
    '+': lambda *args: sum(args),
    '-': lambda *args: reduce(operator.sub, args, 0),
    '*': lambda *args: reduce(operator.mul, args, 1),
    '/': lambda *args: reduce(operator.div, args),
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

    def fetch_scopes(self):
        return self.scopes