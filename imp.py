import cPickle as pickle
from os.path import isfile
from time import time

from nltk.grammar import CFG
from nltk.parse.generate import generate

from learners import PrimalLearner


def test_import():
    print "it worked!"


def code_to_string(code):
    return ''.join(code)


def create_learner():
    if isfile("imp_learner.p"):
        learner_file = open("imp_learner.p", "rb")
        learner = pickle.load(learner_file)
        learner_file.close()
        return learner
    else:
        grammar = CFG.fromstring("""
                Pgm -> Id ',' Pgm | Stmt
                Stmt -> Block | Id '=' Aexp ';' | Stmt Stmt
                Stmt -> 'if(' Bexp ')' Block 'else' Block
                Stmt -> 'while(' Bexp ')' Block
                Block -> '{}' | '{' Stmt '}'
                Bexp -> 'true' | Aexp '<=' Aexp | '!' Bexp
                Bexp -> Bexp '&&' Bexp | Bexp '||' Bexp | '(' Bexp ')'
                Aexp -> Int | Id | Aexp '+' Aexp | Aexp '-' Aexp
                Aexp -> Aexp '*' Aexp | Aexp '/' Aexp | '(' Aexp ')'
                Id -> 'a' | 'b' 
                Bool -> 'true' | 'false'
                Int -> '0' | '1' 
            """)
        return PrimalLearner.from_grammar(grammar, k=1)


def run_trial(learner):
    start_time = time()
    learner.guess(verbose=True)
    end_time = time()
    print "Time Elapsed: {:.2f} seconds".format(end_time - start_time)

    # learner_file = open("imp_learner.p", "wb")
    # pickle.dump(learner, learner_file)
    # learner_file.close()


def run_trials(learner):
    print "Start Learning"
    for _ in range(10):
        run_trial(learner)
    print "Learning Complete\n"


def test_learner(learner):
    print "Generate from Current Guess:"
    for p in generate(learner.get_curr_guess(), depth=3):
        print code_to_string(p)


print "what's going on "
