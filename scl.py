class Sentence(object):
    """
    A sentence.
    """

    def __init__(self, words):
        """
        Initialize from a list of words.

        :type words: list
        :param words: A list of words
        """
        self._words = words

    def get_words(self):
        """
        Public accessor for self._words.

        :rtype: list
        :return: self._words
        """
        return self._words

    def __add__(self, other):
        if type(other) is Sentence:
            return Sentence(self._words + other.get_words())
        elif type(other) is SentenceSet:
            return SentenceSet([self + s for s in other])
        else:
            raise TypeError("Summands must be Sentences or SentenceSets.")

    def to_string(self):
        """
        Converts this Sentence to a string.

        :rtype: str
        :return: This Sentence, as a string
        """
        return " ".join(self._words)

    @staticmethod
    def from_string(string):
        """
        Instantiates a Sentence from a string.

        :type string: str
        :param string: A string

        :rtype: Sentence
        :return: A Sentence
        """
        return Sentence(string.split(" "))

    def __str__(self):
        return self.to_string()


class SentenceSet(object):
    """
        A set of Sentences, since they are not hashable.
    """

    def __init__(self, sentences):
        """
        Initialize from a list of Sentences.

        :type sentences: list
        :param sentences: A list of Sentences.
        """
        self._sentences = set([s.to_string() for s in sentences])
        self._name = None

    def __iter__(self):
        for s in self._sentences:
            yield Sentence.from_string(s)

    def get_sentences(self):
        """
        Public accessor for self._sentences.

        :rtype: set
        :return: self._sentences
        """
        return self._sentences

    def set_sentences(self, sentences):
        """
        Public mutator for self._sentences.

        :type sentences: set
        :param sentences: The value to set self._sentences to

        :rtype NoneType
        :return: None
        """
        self._sentences = sentences

    def get_name(self):
        """
        Get the name of this SentenceSet.

        :return: self._name
        """
        return self._name

    def set_name(self, name):
        """
        Assign a name to this SentenceSet.

        :param name: A name for this SentenceSet

        :rtype: NoneType
        :return: None
        """
        self._name = name

    def __contains__(self, sentence):
        """
        Check if this SentenceSet contains a sentence.

        :type sentence: Sentence
        :param sentence: A sentence

        :rtype: bool
        :return: Whether or not this SentenceSet contains sentence.
        """
        return sentence.to_string() in self._sentences

    def add(self, sentence):
        """
        Adds a sentence to this SentenceSet.

        :type sentence: Sentence
        :param sentence: A Sentence

        :rtype: NoneType
        :return: None
        """
        self._sentences.add(sentence.to_string())

    def union(self, sentenceset):
        """
        Computes the union of this with another SentenceSet.

        :type sentenceset: SentenceSet
        :param sentenceset: Another SentenceSet

        :rtype: SentenceSet
        :return: The union of the two SentenceSets.
        """
        new = SentenceSet([])
        new.set_sentences(self._sentences.union(sentenceset.get_sentences()))
        return new

    def update(self, sentenceset):
        """
        Unions another SentenceSet into this one.

        :type sentenceset: SentenceSet
        :param sentenceset: Another SentenceSet

        :rtype: NoneType
        :return: None
        """
        self._sentences.update(sentenceset.get_sentences())

    def __add__(self, other):
        if type(other) is SentenceSet:
            return SentenceSet([s + t for s in self for t in other])
        elif type(other) is Sentence:
            return SentenceSet([s + other for s in self])
        else:
            raise TypeError("Summands must be Sentences or SentenceSets.")


class Context(object):
    """
    A 2D context.
    """

    def __init__(self, left, right):
        """
        Initialize by specifying the left and right sides.

        :type left: list
        :param left: The left side

        :type right: list
        :param right: The right side
        """
        self._left = left
        self._right = right

    def wrap(self, sentence):
        """
        The wrap operator

        :type sentence: Sentence
        :param sentence: A Sentence

        :rtype: Sentence
        :return: The context wrapped around the sentence
        """
        if type(sentence) is not Sentence:
            raise TypeError("Context.wrap must be used for Sentences.")

        return Sentence(self._left + sentence.get_words() + self._right)

    def wrap_set(self, sentenceset):
        """
        The wrap operator for a set of sentences

        :type sentenceset: SentenceSet
        :param sentenceset: A set of sentences

        :rtype: SentenceSet
        :return: The context wrapped around sentenceset
        """
        if type(sentenceset) is not SentenceSet:
            raise TypeError("Context.wrap_set must be used for SentenceSets.")

        return SentenceSet([self.wrap(s) for s in sentenceset])

    def to_string_tuple(self):
        """
        Converts this Context to a tuple of strings.

        :rtype: tuple
        :return: This context as a tuple of strings
        """
        return " ".join(self._left), " ".join(self._right)

    @staticmethod
    def from_string_tuple(string_tuple):
        """
        Instantiates a Context from a tuple of strings.

        :type string_tuple: tuple
        :param string_tuple: A tuple of strings

        :rtype: Context
        :return: A context
        """
        left = string_tuple[0].split(" ")
        right = string_tuple[1].split(" ")
        return Context(left, right)

    def __str__(self):
        return str(self.to_string_tuple())


class ContextSet(object):
    """
    A set of Contexts, since Contexts are not hashable.
    """

    def __init__(self, contexts):
        """
        Initialize from a list of Contexts.

        :type contexts: list
        :param contexts: A list of Contexts.
        """
        self._contexts = set([c.to_string_tuple() for c in contexts])
        self._name = None

    def __iter__(self):
        for c in self._contexts:
            yield Context.from_string_tuple(c)

    def get_contexts(self):
        """
        Public accessor for self._contexts

        :rtype: set
        :return: self._contexts
        """
        return self._contexts

    def set_contexts(self, contexts):
        """
        Public mutator for self._contexts

        :type contexts: set
        :param contexts: The value to set self._contexts to

        :rtype: NoneType
        :return: None
        """
        self._contexts = contexts

    def get_name(self):
        """
        Get the name of this ContextSet.

        :return: self._name
        """
        return self._name

    def set_name(self, name):
        """
        Assign a name to this ContextSet.

        :param name: A name for this ContextSet

        :rtype: NoneType
        :return: None
        """
        self._name = name

    def __contains__(self, context):
        """
        Check if this ContextSet contains a context.

        :type context: Context
        :param context: A context

        :rtype: bool
        :return: Whether or not this ContextSet contains context.
        """
        return context.to_string_tuple() in self._contexts

    def add(self, context):
        """
        Adds a context to this ContextSet.

        :type context: Context
        :param context: A Context

        :rtype: NoneType
        :return: None
        """
        self._contexts.add(context.to_string_tuple())

    def union(self, contextset):
        """
        Computes the union of this with another ContextSet.

        :type contextset: ContextSet
        :param contextset: Another ContextSet

        :rtype: ContextSet
        :return: The union of the two ContextSets.
        """
        new = ContextSet([])
        new.set_contexts(self._contexts.union(contextset.get_contexts()))
        return new

    def update(self, contextset):
        """
        Unions another ContextSet into this one.

        :type contextset: ContextSet
        :param contextset: Another ContextSet

        :rtype: NoneType
        :return: None
        """
        self._contexts.update(contextset.get_contexts())

    def wrap(self, sentence):
        """
        Wraps this ContextSet around a Sentence.

        :type sentence: Sentence
        :param sentence: A Sentence

        :rtype: SentenceSet
        :return: This ContextSet wrapped around sentence
        """
        if type(sentence) is not Sentence:
            raise TypeError("ContextSet.wrap must be used for Sentences.")

        return SentenceSet([c.wrap(sentence) for c in self])

    def wrap_set(self, sentenceset):
        """
        Wraps this Context around a set of Sentences.

        :type sentenceset: SentenceSet
        :param sentenceset: A set of Sentences

        :rtype: SentenceSet
        :return: This ContextSet wrapped around sentenceset
        """
        if type(sentenceset) is not SentenceSet:
            raise TypeError("ContextSet.wrap_set must be used for SentenceSets.")

        result = SentenceSet([])
        for s in sentenceset:
            result.update(self.wrap(s))

        return result
