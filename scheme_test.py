import unittest
from parser import tokenize, parser, read
from scheme import Environment, Evaluator


class TestParser(unittest.TestCase):

  line = '((lambda(x) x) "Lisp")'

  def test_x(self):
    self.assertEqual(tokenize('x'), ['x'])

  def test_x_read(self):
    self.assertEqual(parser(tokenize('x')), ['x'])

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

  def test_eval(self):
    exp = Evaluator().eval('x')
    self.assertEqual(exp, None)

    exp = Evaluator().eval('x', Environment([{'x': 1}]))
    self.assertEqual(exp, 1)

    exp = Evaluator().eval('"foo"')
    self.assertEqual(exp, '"foo"')

    exp = Evaluator().eval(-5)
    self.assertEqual(exp, -5)

    exp = Evaluator().eval(['quote', '"foo"'])
    self.assertEqual(exp, '"foo"')

    exp = Evaluator().eval(['+', 1, 1])
    self.assertEqual(exp, 2)

    exp = Evaluator().eval(['if', ['<', 1, 2], '#t', '#f'])
    self.assertEqual(exp, True)

    exp = Evaluator().eval(['lambda', ['x'], 'x'])
    self.assertIsInstance(exp, type(lambda: None))
    self.assertEqual(exp(1), 1)

    exp = Evaluator().eval(read('(let ((x 4)) x)'))
    self.assertEqual(exp, 4)

    exp = Evaluator().eval(read('(let ((x 4)) (let ((x 3)) x))'))
    self.assertEqual(exp, 3)

    exp = Evaluator().eval(read('(let ((x 4)) (let ((x 3)) "foo" x))'))
    self.assertEqual(exp, 3)


    e = Evaluator()
    exp = e.eval(read('(define x 4)'))
    self.assertEqual(e.env.get('x'), 4)



if __name__ == '__main__':
  unittest.main()