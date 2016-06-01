from pyparsing import CharsNotIn
from pyparsing import Forward
from pyparsing import Group
from pyparsing import nums
from pyparsing import StringEnd
from pyparsing import StringStart
from pyparsing import Suppress
from pyparsing import Word
from pyparsing import ZeroOrMore
import six


def to_int_action(toks):
    """Convert first token to integer"""
    return int(toks[0])

# general parsers for all expressions
exprParser = Forward()


#################
# String Parser #
#################
# String is formated as:
# <length of string>:<string>

# Since second part of the parser is using the result from
# the first part, we are creating a lazy parser and create second part
# of the parser after we parse the length.
actualStrParser = Forward()


# After first part is parsed, Create second parser with the data
# from the first part.
def str_parse_action(s, l, t):
    n = t[0]
    actualStrParser << CharsNotIn('', exact=n)
    # since we do not need lenght of the parser anymore
    # we can ignore it.
    return []

# strLength parser parses length of the string
# <length of string>:
strLengthParser = Word(nums) + Suppress(':')
strLengthParser.setParseAction(to_int_action)
# after length is parsed create second part of the parser.
strLengthParser.addParseAction(str_parse_action, callDuringTry=True)
# Actual str parser is lenghtParser + ActualStrParser
strParser = strLengthParser + actualStrParser


##############
# Int Parser #
##############
# Integer is formated as
# i<integer>e
intParser = Suppress('i') + Word(nums) + Suppress('e')
intParser.setParseAction(to_int_action)


###############
# List Parser #
###############
# List is formated as
# l[value 1][value2][value3][...]e
def list_parse_action(toks):
    return [toks.asList()]

listParser = Suppress('l') + ZeroOrMore(exprParser) + Suppress('e')
listParser.setParseAction(list_parse_action)


#####################
# Dictionary Parser #
#####################
# Dictionary is formated as
# d[key1][value1][key2][value2][...]e
def dict_parse_action(toks):
    """Convert list of key, value tuples to dictionary"""
    return [dict(toks.asList())]

dictParser = (Suppress('d') +
              ZeroOrMore(Group(exprParser + exprParser)) +
              Suppress('e'))
# TODO can we use dict of?
dictParser.setParseAction(dict_parse_action)

# expr can be int, str, list or dictionary
exprParser << (intParser | strParser | listParser | dictParser)

# parser that matches the whole string
parser = StringStart() + exprParser + StringEnd()


def decode(st):
    resp = parser.parseString(st)
    return resp[0]


def encode(obj):
    """Encoder for bencode format."""
    if isinstance(obj, int):
        # 123 => i123e
        resp = 'i%se' % obj
    elif isinstance(obj, six.string_types):
        # 'abc' => 3:abc
        resp = '%s:%s' % (len(obj), obj)
    elif isinstance(obj, list):
        # [1, 2, 3] => li1ei2ei3ee
        resp = 'l%se' % ''.join(encode(i) for i in obj)
    elif isinstance(obj, dict):
        # {'key': 'value'} => d3:key5:valuee
        resp = 'd%se' % ''.join(encode(i)
                                for kv in obj.items()
                                for i in kv)
    else:
        raise ValueError('type "%s" is not supported: %s' % (type(obj), obj))

    return resp
