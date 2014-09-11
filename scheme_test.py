import unittest
from scheme import tokenize, parser, read


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





if __name__ == '__main__':
  unittest.main()