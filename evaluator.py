from identity import *
from parser import read
from environment import Environment

class Evaluator(object):

    def __init__(self):
        self.env = Environment([{}])
  

    def eval(self, exp, env=None):
        print exp
        if not env == None:
            print env.fetch_scopes() 
        print 'foos'
        if env == None:
            print 'no env'
            return self.eval(exp, self.env)
        elif is_symbol(exp):
            print 'ajsjd'
            return env.get(exp)
        elif is_string(exp):
            print 'str'
            return exp
        elif is_number(exp):
            print 'num'
            return exp
        elif is_quote(exp):
            print 'is_quote'
            (_, x) = exp
            return x
        elif is_if(exp):
            print 'is_if'
            (_, test, truthy, falsy) = exp
            return self.eval((truthy if self.eval(test) else falsy), env)
        elif is_let(exp):
            print 'let'
            variables = exp[1]
            exprs = exp[2:]
            (names, vals) = map(lambda L: list(L), list(zip(*variables)))
            exp = ['lambda', names]
            exp += exprs
            return self.eval_lambda(exp, env)(*vals)
        elif self.is_primitive(exp):
            print 'is_primitive'
            return self.eval_primitive(exp)
        elif is_lambda(exp):
            print 'lambda'
            return self.eval_lambda(exp, env)
        elif is_define(exp):
            print 'is_define'
            variable = exp[1]
            value = exp[2]
            env.set(variable, self.eval(value, env))
        else:
            print 'bar'
            func = self.eval(exp[0], env)
            return func(*[self.eval(x, env) for x in exp[1:]])

    def eval_lambda(self, exp, env):
        variables = exp[1]
        exprs = exp[2:]
        new_env = env.create()
        def lambda_func(*args):
            print 'lambda_func'
            assert len(args) == len(variables), 'Something wrong happened'
            new_env.add_scope()
            for param, arg in zip(variables, args):
                new_env.set(param, arg)
            return ([self.eval(x, new_env) for x in exprs])[-1]
        return lambda_func


    def is_primitive(self, exp):
        print
        print exp
        print exp[0]
        if exp[0] in primitives:
            print 'foo'
            return True
        # return exp[0] in primitives
      

    def eval_primitive(self, exp):
        return primitives[exp[0]](exp)


def is_it_equal(exp):
    (_, first_val, second_val) = exp
    return first_val == second_val

primitives = {
    'eq?': is_it_equal
}
