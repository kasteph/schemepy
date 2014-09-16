import unittest
from scheme import tokenize, parser, read, Environment, eval


class TestScheme(unittest.TestCase):

  line = '((lambda(x) x) "Lisp")'

  def test_tokenize(self):
    self.assertEqual(tokenize(self.line), ['(', '(', 'lambda', '(', 'x', ')', 'x', ')', '"Lisp"', ')'])

  def test_parser(self):
    self.assertEqual(parser(tokenize(self.line)), [['lambda', ['x'], 'x'], '"Lisp"'])

  def test_read_simple_expression(self):
    self.assertEqual(read('(1 2)'), ['1', '2'])

  def test_read_simple_lambda(self):
    self.assertEqual(read(self.line), [['lambda', ['x'], 'x'], '"Lisp"'])

  def test_environment(self):
    a = Environment([{}])

    self.assertEqual(a.get('x'), None)
    
    a.set('x', 1)
    self.assertEqual(a.get('x'), 1)

    a.add_scope()
    a.set('x', 2)

    self.assertEqual(a.get('x'), 2)

    a.remove_scope()

    self.assertEqual(a.get('x'), 1)




if __name__ == '__main__':
  unittest.main()