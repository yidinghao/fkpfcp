from abc import ABCMeta, abstractmethod

from nltk import CFG, ChartParser
from nltk.parse.generate import generate

from scl import Sentence


class Text(object):
    """
    A text.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        self._iterator = None

    @abstractmethod
    def __iter__(self):
        return self._iterator


class GrammarText(Text):
    """
    A text from a grammar.
    """

    def __init__(self, grammar):
        """
        Initialize from a CFG.

        :type grammar: CFG
        :param grammar: A CFG generating the text.
        """
        super(GrammarText, self).__init__()
        self._iterator = generate(grammar)

    def __iter__(self):
        for i in self._iterator:
            yield Sentence(i)


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
