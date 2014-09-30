import sys

from parser import read
from evaluator import Evaluator

def REPL(line, evaluator):
    try:
        return evaluator.eval(read(line))
    except IndexError:
        return ''


if __name__ == '__main__':
    print 'Welcome to schemepy. Press <Ctrl-c> to exit.'
    e = Evaluator()
    while True:
        try:
            scheme = raw_input()
            print REPL(scheme, e)
        except (KeyboardInterrupt, SystemExit):
            print 'Exiting schemepy.'
            sys.exit()
