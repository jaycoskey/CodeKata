#!/usr/bin/env python

import argparse
from collections import Counter
from dataclasses import dataclass
import itertools
import re
import string
import sys
from typing import List
import unittest


XWORD_HELP = r"""
  Allow user to specify constraints and word files for crossword puzzles. Specifically,
  the user can specify a list of pattern constraints for the answers, including which
  letters in a given answer must match which other letters in another answer.

  Each constraint in the constraints input file is a string of characters where:
    - Letters (lower or upper case) represent characters as they must be in each answer.
    - Asterisks (*) represent free (i.e., unconstrained) letters.
    - Digits (0-9) represent letters that must match the letters used in other answers.
      (A constraints file with more than ten such tags would likely have a very long runtime.
      This script does not lend itself to solving an entire crossword puzzle.)

  Example #1:
    * There are two answers: 5 letters starting with a 'T', and 4 letters starting with a 'W'.
    * They intersect at the first answer's fourth letter, and the first answer's second.
    * Then the constraints could be written as:
        T**3*
        W3**
      These constraints have many solutions, one of them being "TIDAL" and "WAVE".
  Example #2:
    * The constraints
        L1....2M
        N3....4O
        D1....3E
        F2.C..4G
      are satisfied by the following words:
        LUKEWARM
        NEUTRINO
        DUNGAREE
        FRACKING
 
  Some intersection scenarios have no solutions, while others have a huge number of solutions.
  Execution time can rise rapidly with the number of answers/constraints, but can also remain small if each constraint
    only has a small number of answers that satisfy it.
  To aid in crossword puzzle authoring, proper nouns can be added to the wordlist.
  For themed crosswords, words or phrases relevant to the theme can be added to the wordlist.
"""
# Developer note: Numeric matched wildcards are called xvars. The possible values are called xvals.
# TODO: Add check to ensure that each intersection variable appears no more than once in a given constraint.
# TODO: Provide option to print answers mostly in one case, but with xvals printed in the other case.

DEFAULT_CONSTRAINTS_FILE = './constraints.puz'
DEFAULT_WORDS_FILE = '/usr/share/dict/words'


# Stores the data regarding the intersections of two answers
# Used to test a candidate solutions, to see whether the intersection letters match
@dataclass
class XvarData:
    constraint0: int
    pos0: int
    constraint1: int
    pos1: int

 
# Note: Constraint strings have already been converted to lowercase.
def get_regexpr_str(constraint: str):
    constraint = constraint.replace('*', '.')
    for digit in range(0, 10):
        constraint = constraint.replace(str(digit), '.')
    return '^' + constraint + '$'

# Each xval must match the corresponding positions in the crossing answers.
def get_solutions(answers: List[List[str]], xvardatas: List[XvarData]):
    for candidate in itertools.product(*answers):
        for xvd in xvardatas:
            if candidate[xvd.constraint0][xvd.pos0] != candidate[xvd.constraint1][xvd.pos1]:
                break
        else:
            yield candidate
    return

def get_xvardatas(constraints: List[str], xvars: List[int]):
    xvardatas: List[XvarData] = []
    for xvar_k in range(len(xvars)):
        is_first_found = False
        for constraint_k in range(len(constraints)):
            xvar_pos = constraints[constraint_k].find(str(xvars[xvar_k]))
            if xvar_pos != -1:
                if is_first_found:
                    xvardatas[xvar_k].constraint1 = constraint_k
                    xvardatas[xvar_k].pos1 = xvar_pos
                    continue  # Found second and final constrainted word
                else:
                    xvd = XvarData(constraint_k, xvar_pos, -1, -1)
                    xvardatas.append(xvd)
                    is_first_found = True
    return xvardatas    

# Given a list of constraints, return the answer intersection variables (digits) that appear.
# If each intersection variable does not appear exactly twice, print an error message and raise a ValueError.
#
def get_xvars(constraints: List[str]):
    digits = [c for word in constraints for c in word if c in '0123456789']
    digit_hist = Counter(digits)
    if not all([v == 2 for v in digit_hist.values()]):
        violators = [k for k,v in digit_hist.items() if v != 2]
        violators_str = ', '.join(sorted(violators))
        print(f'These answer intersection variables do not appear in pairs: {violators_str}', file=sys.stderr)
        raise ValueError(f'get_xvars: Variable count error(s): {violators_str}')
    return sorted(sorted(digit_hist.keys()))

def is_scrabble_word(word):
    return all([c in string.ascii_lowercase for c in word.rstrip()])

def is_xvardata_valid(x):
    return x.constraint0 >= 0 and x.pos0 >= 0 and x.constraint1 >= 0 and x.pos1 >= 0

def main(words_file, constraints_file):
    constraints = [line.rstrip().lower() for line in open(constraints_file, 'r').readlines()]
    regexpr_strs = [get_regexpr_str(constraint) for constraint in constraints]
    regexprs = [re.compile(s) for s in regexpr_strs]
    with open(words_file, 'r') as f:
        words = [word.replace('\n', '').rstrip() for word in f.readlines() if is_scrabble_word(word)]
    xvars = get_xvars(constraints)

    # Each answer (one per constraint) must be in the wordlist and match the corresponding constraint.
    answers = [[w.upper() for w in words if re.search(regexprs[k], w)]
                  for k in range(len(constraints))
              ]
    xvardatas = get_xvardatas(constraints, xvars)
    for k, soln in enumerate(get_solutions(answers, xvardatas)):
        print(f'Solution #{k+1:2}: {soln}')


class TestXwordFunctions(unittest.TestCase):
    def test_get_regexpr_str(self):
        self.assertTrue(get_regexpr_str('ab.5e'), '^ab..e$')
    
    def test_get_solutions(self):
        answers = [['tidal', 'wave'], ['total', 'when']]
        xvardatas = [XvarData(0, 3, 1, 1)]
        self.assertTrue(get_solutions(answers, xvardatas), [['tidal', 'wave']])

    def test_get_xvardatas(self):
        self.assertTrue(get_xvardatas(['T**3*', 'W3**'], [3]), [XvarData(0, 3, 1, 1)])

    def test_get_xvars(self):
        self.assertTrue(get_xvardatas(['T**3*', 'W3**'], [3]))


# TODO: Modify to allow multiple wordlists (e.g., standard dictionary + theme words + theme phrases)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Allow user to specify constraints and word files for crossword puzzles .\n' + XWORD_HELP,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-c', '--constraints', type=str,
            help='Specify path of constraints file [Default is ./constraints.puz]')
    parser.add_argument('-w', '--words', type=str,
            help='Specify path of words file')
    parser.add_argument('-t', '--tests', action='store_true',
            help='Run unit tests before finding solutions [Default is /usr/share/dict/words]')
    args = parser.parse_args()

    constraints_file = args.constraints if args.constraints else DEFAULT_CONSTRAINTS_FILE    
    do_run_tests = args.tests
    words_file = args.words if args.words else DEFAULT_WORDS_FILE

    if do_run_tests:
        unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestXwordFunctions))

    main(words_file, constraints_file)
