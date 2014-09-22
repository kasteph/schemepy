from evaluator import Evaluator

def REP(line, evaluator):
  return evaluator.eval(read(line))


if __name__ == '__main__':

  e = Evaluator()
  while True:
    scheme = raw_input()
    print REP(scheme, e)
