from forms import *
from parser import read
from environment import Environment

class Evaluator(object):

    def __init__(self):
        self.env = Environment([{}])
  

    def eval(self, exp, env=None):
        if env == None:
            return self.eval(exp, self.env)
        elif is_symbol(exp):
            return env.get(exp)
        elif is_string(exp):
            return exp
        elif is_number(exp):
            return exp
        elif is_quote(exp):
            (_, x) = exp
            return x
        elif is_if(exp):
            (_, test, truthy, falsy) = exp
            return self.eval((truthy if self.eval(test) else falsy), env)
        elif is_let(exp):
            variables = exp[1]
            exprs = exp[2:]
            (names, vals) = map(lambda L: list(L), list(zip(*variables)))
            exp = ['lambda', names]
            exp += exprs
            return self.eval_lambda(exp, env)(*vals)
        elif is_lambda(exp):
            return self.eval_lambda(exp, env)
        elif is_define(exp):
            variable = exp[1]
            value = exp[2]
            env.set(variable, self.eval(value, env))
        elif exp[0] in ['eqv?']:
            return special_form(exp)
        else:
            func = self.eval(exp[0], env)
            return func(*[self.eval(x, env) for x in exp[1:]])

    def eval_lambda(self, exp, env):
        variables = exp[1]
        exprs = exp[2:]
        new_env = env.create()
        def lambda_func(*args):
            assert len(args) == len(variables), 'Something wrong happened'
            new_env.add_scope()
            for param, arg in zip(variables, args):
                new_env.set(param, arg)
            return ([self.eval(x, new_env) for x in exprs])[-1]
        return lambda_func


