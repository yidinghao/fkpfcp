from abc import ABCMeta, abstractmethod
from itertools import combinations

from nltk.grammar import CFG, Nonterminal, Production

import oracles
from scl import Sentence, SentenceSet, Context, ContextSet


class Learner(object):
    """
    Encapsulates state for learning algorithms.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        self._text = None
        self._oracle = None
        self._curr_guess = None

    def __iter__(self):
        return self

    def next(self):
        return self.guess()

    @abstractmethod
    def guess(self):
        """
        Makes a guess based on the next observation.
        Updates self._curr_guess.

        :rtype: CFG
        :returns: The next guess
        """
        return None

    def get_curr_guess(self):
        """
        Public accessor for the current guess.

        :rtype: CFG
        :return: self._curr_guess
        """
        return self._curr_guess


class PrimalLearner(Learner):
    """
        Implementation of the primal algorithm of Yoshinaka (2011).
    """

    def __init__(self, text, oracle, k):
        """
        Initialize from a Text and an Oracle.

        :type text: oracles.Text
        :param text: A text

        :type oracle: oracles.Oracle
        :param oracle: An oracle

        :type k: int
        :param k: The grammar learned will have the k-FKP.
        """
        super(PrimalLearner, self).__init__()
        self._text = text
        self._oracle = oracle
        self._k = k

        # Algorithm state
        self._data = SentenceSet([])
        self._substrings = SentenceSet([])
        self._contexts = ContextSet([])

        # Current guess
        self._name_ctr = 0
        self._kernels = []
        self._nonterminals = dict()
        self._terminals = set()
        self._productions = set()
        self._start_symbol = Nonterminal(-1)
        self._curr_guess = None

    def _new_name(self):
        self._name_ctr += 1
        return self._name_ctr - 1

    def guess(self):
        sentence = next(self._text)
        if sentence in self._data:
            return self._curr_guess

        # Update data and terminals
        words = sentence.get_words()
        self._data.add(sentence)
        self._terminals.update(set(sentence.get_words()))

        # Update contexts
        for i in range(len(words)):
            for j in range(i, len(words)):
                self._contexts.add(Context(words[:i], words[j:]))

        # Update substrings
        is_new_sentence = not self._oracle.generates(sentence)
        if is_new_sentence:
            for i in range(len(words)):
                for j in range(i, len(words)):
                    self._substrings.add(Sentence(words[i:j]))

        # Construct the nonterminals
        kernels = set()
        for i in range(self._k + 1):
            subsets = [SentenceSet(j) for j in combinations(self._substrings, i)]
            kernels.update(subsets)

        for k in kernels:
            if k not in self._nonterminals:
                self._nonterminals[k] = Nonterminal(self._new_name())

        # Construct the rules
        self._productions = set()
        for kernel in kernels:
            contexts = self._oracle.restr_right_triangle(kernel, self._contexts)
            nt = self._nonterminals[kernel]

            # Lexical rules
            for t in self._terminals:
                add_lexical_rule = True
                for s in contexts.wrap(Sentence([t])):
                    if not self._oracle.generates(s):
                        add_lexical_rule = False
                        break

                if add_lexical_rule:
                    rule = Production(nt, [Nonterminal(t)])
                    self._productions.add(rule)

            # Binary rules
            for s1 in kernels:
                for s2 in kernels:
                    add_binary_rule = True
                    for s in contexts.wrap_set(s1 + s2):
                        if not self._oracle.generates(s):
                            add_binary_rule = False
                            break

                    if add_binary_rule:
                        nt1 = self._nonterminals[s1]
                        nt2 = self._nonterminals[s2]
                        rule = Production(nt, [nt1, nt2])
                        self._productions.add(rule)

            # Start rules
            add_start_rule = True
            for s in kernel:
                if not self._oracle.generates(s):
                    add_start_rule = False
                    break

            if add_start_rule:
                rule = Production(self._start_symbol, [nt])
                self._productions.add(rule)

        # Construct the grammar
        self._curr_guess = CFG(self._start_symbol, self._productions)
        return self._curr_guess
