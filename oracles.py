from abc import ABCMeta, abstractmethod

from nltk import CFG, ChartParser
from nltk.parse.generate import generate

from scl import Sentence, ContextSet, SentenceSet


class Text(object):
    """
    A text.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def next(self):
        pass


class GrammarText(Text):
    """
    A text from a grammar.
    """

    def __init__(self, grammar, depth=5):
        """
        Initialize from a CFG.

        :type grammar: CFG
        :param grammar: A CFG generating the text.
        """
        self._iterator = generate(grammar, depth=depth)

    def __iter__(self):
        return self

    def next(self):
        return next(self._iterator)


class Oracle(object):
    """
    An oracle.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def generates(self, sentence):
        """
        A function deciding language membership.

        :type sentence: Sentence
        :param sentence: A sentence

        :rtype: bool
        :return: Whether or not the oracle accepts sentence
        """
        return False

    def restr_right_triangle(self, sentences, contexts):
        result = ContextSet([])
        for c in contexts:
            is_valid_context = True
            for s in c.wrap_set(sentences):
                if not self.generates(s):
                    is_valid_context = False
                    break

            if is_valid_context:
                result.add(c)

        return result

    def restr_left_triangle(self, contexts, sentences):
        result = SentenceSet([])
        for s in sentences:
            is_valid_substring = True
            for t in contexts.wrap(s):
                if not self.generates(t):
                    is_valid_substring = False
                    break

            if is_valid_substring:
                result.add(s)

        return result


class GrammarOracle(Oracle):
    """
    An oracle from a grammar.
    """

    def __init__(self, grammar):
        """
        Initialize from a CFG.

        :type grammar: CFG
        :param grammar: The grammar for this oracle
        """
        self._parser = ChartParser(grammar)

    def generates(self, sentence):
        """
        Decides whether the grammar generates the sentence.

        :type sentence: Sentence
        :param sentence: A sentence

        :rtype: bool
        :return: Whether the grammar generates the sentence
        """
        try:
            parses = self._parser.parse(sentence.get_words())
            return list(parses) != []
        except:
            return False
