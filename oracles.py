from nltk import CFG, ChartParser


def generates(sentence, grammar=None, parser=None):
    """
    Check whether or not a grammar generates a string.

    :type grammar: CFG
    :param grammar: The grammar to parse from

    :type sentence: list
    :param sentence: The sentence to parse

    :param parser: A parser for the grammar (optional)

    :rtype: bool
    :return: Whether or not grammar generates sentence
    """
    if grammar is None and parser is None:
        raise ValueError("A grammar or a parser is required.")
    if parser is None:
        parser = ChartParser(grammar)

    try:
        parses = parser.parse(sentence)
        return list(parses) != []
    except:
        return False
