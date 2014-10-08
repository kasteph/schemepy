import unittest
from parser import tokenize, parser, read
from environment import Environment
from evaluator import Evaluator


class TestParser(unittest.TestCase):

    line = '((lambda(x) x) "Lisp")'

    def test_x(self):
        self.assertEqual(tokenize('x'), ['x'])

    def test_x_read(self):
        self.assertEqual(parser(tokenize('x')), 'x')

    def test_tokenize(self):
        self.assertEqual(tokenize(self.line), ['(', '(', 'lambda', '(', 'x', ')', 'x', ')', '"Lisp"', ')'])

    def test_parser(self):
        self.assertEqual(parser(tokenize(self.line)), [['lambda', ['x'], 'x'], '"Lisp"'])

    def test_read_number_list(self):
        self.assertEqual(read('(1 2 3.14 22.22)'), [1, 2, 3.14, 22.22])

    def test_read_simple_lambda(self):
        self.assertEqual(read(self.line), [['lambda', ['x'], 'x'], '"Lisp"'])


class TestEnvironment(unittest.TestCase):

    def test_environment(self):
        env = Environment([{}])
        self.assertEqual(env.get('x'), None)

        env.set('x', 1)
        self.assertEqual(env.get('x'), 1)

        env.set('y', 'foo')
        self.assertEqual(env.get('y'), 'foo')
        self.assertEqual(env.get('x'), 1)

        env.add_scope()
        env.set('x', 2)
        self.assertEqual(env.get('x'), 2)

        env.remove_scope()
        self.assertEqual(env.get('x'), 1)


class TestEval(unittest.TestCase):

    def test_undefined_variable(self):
        exp = Evaluator().eval('x')
        self.assertEqual(exp, None)

    def test_getting_variable_value(self): 
        exp = Evaluator().eval('x', Environment([{'x': 1}]))
        self.assertEqual(exp, 1)

    def test_eval_string(self):
        exp = Evaluator().eval('"foo"')
        self.assertEqual(exp, '"foo"')

    def test_eval_int(self):
        exp = Evaluator().eval(-5)
        self.assertEqual(exp, -5)

    def test_eval_float(self):
        exp = Evaluator().eval(3.14)
        self.assertEqual(exp, 3.14)

    def test_eval_quote(self):
        exp = Evaluator().eval(['quote', '"foo"'])
        self.assertEqual(exp, '"foo"')

    def test_eval_plus(self):
        exp = Evaluator().eval(['+', 1, 1])
        self.assertEqual(exp, 2)

    def test_eval_if(self):
        exp = Evaluator().eval(['if', ['<', 1, 2], '#t', '#f'])
        self.assertEqual(exp, True)

    def test_lambda_is_func_and_evals_exp(self):
        exp = Evaluator().eval(['lambda', ['x'], 'x'])
        self.assertIsInstance(exp, type(lambda: None))
        self.assertEqual(exp(1), 1)

    def test_lamda_expression(self):
        exp = Evaluator().eval(read('(lambda (x) (+ x 2))'))
        self.assertIsInstance(exp, type(lambda: None))

    def test_eval_lambda_expression(self):
        exp = Evaluator().eval(read('((lambda(x) (+ x 2)) 42)'))
        self.assertEqual(exp, 44)

    def test_eval_simple_let(self):
        exp = Evaluator().eval(read('(let ((x 4)) x)'))
        self.assertEqual(exp, 4)

    def test_eval_nested_let(self):
        exp = Evaluator().eval(read('(let ((x 4)) (let ((x 3)) x))'))
        self.assertEqual(exp, 3)

    def test_eval_let_with_two_vals_in_last_sexp(self):
        exp = Evaluator().eval(read('(let ((x 4)) (let ((x 3)) "foo" x))'))
        self.assertEqual(exp, 3)

    def test_define_var(self):
        e = Evaluator()
        exp = e.eval(read('(define x 4)'))
        self.assertEqual(e.env.get('x'), 4)

    def test_define_lambda(self):
        e = Evaluator()
        exp = e.eval(read('(define square (lambda (x)  (* x x)))'))
        next_exp = e.eval(read('(square 5)'))
        self.assertEqual(next_exp, 25)

    def test_define_func(self):
        e = Evaluator()
        exp = e.eval(read('(define (square a) (* a a))'))
        self.assertIsInstance(exp, type(lambda: None))

    def test_eqv_special_form(self):
        e = Evaluator()
        exp = e.eval(read('(eqv? 1 1)'))
        self.assertEqual(exp, True)

    def test_complex_eqv_special_form(self):
        e = Evaluator()
        exp = e.eval(read('(let ((p (lambda (x) x))) (eqv? p p)'))
        self.assertEqual(exp, True)

    def test_falsy_eqv_special_form(self):
        e = Evaluator()
        exp = e.eval(read('(eqv? 1 2)'))
        self.assertEqual(exp, False)


if __name__ == '__main__':
  unittest.main()