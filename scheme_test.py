import unittest
from scheme import tokenize

class TestScheme(unittest.TestCase):

  def test_tokenize(self):
    """
    Test that a line of Scheme will be broken up into 'atoms' or tokens in a list.
    """

    line = tokenize('((lambda(x) x) "Lisp")')
    self.assertEqual(line, ['(', '(', 'lambda', '(', 'x', ')', 'x', ')', '"Lisp"', ')'])


if __name__ == '__main__':
  unittest.main()