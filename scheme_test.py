import unittest
from scheme import tokenize, parser, read, Environment, eval


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

  def test_eval(self):
    exp = eval(['x'])
    self.assertEqual(exp, None)

    exp = eval(['x'], Environment([{'x': 1}]))
    self.assertEqual(exp, 1)

    exp = eval(['"foo"'], Environment([{'_': "foo"}]))
    self.assertEqual(exp, None)

    exp = eval([-5], Environment([{'_': -5}]))
    self.assertEqual(exp, -5)

    # exp = eval('if (boolean? #t) \'foo \'bar')
    # self.assertEqual(exp, True)




if __name__ == '__main__':
  unittest.main()