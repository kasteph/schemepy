import unittest
from parser import tokenize, parser, read
from scheme import Environment, eval


class TestParser(unittest.TestCase):

  line = '((lambda(x) x) "Lisp")'

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
    exp = eval('x')
    self.assertEqual(exp, None)

    exp = eval('x', Environment([{'x': 1}]))
    self.assertEqual(exp, 1)

    exp = eval('"foo"')
    self.assertEqual(exp, '"foo"')

    exp = eval(-5)
    self.assertEqual(exp, -5)

    exp = eval(['quote', '"foo"'])
    self.assertEqual(exp, '"foo"')

    exp = eval(['+', 1, 1])
    self.assertEqual(exp, 2)

    exp = eval(['if', ['<', 1, 2], '#t', '#f'])
    self.assertEqual(exp, True)

    exp = eval(['lambda', ['x'], 'x'])
    self.assertIsInstance(exp, type(lambda: None))
    self.assertEqual(exp(1), 1)

    exp = eval(read('(let ((x 4)) x)'))
    self.assertEqual(exp, 4)

    exp = eval(read('(let ((x 4)) (let ((x 3)) x))'))
    self.assertEqual(exp, 3)


if __name__ == '__main__':
  unittest.main()