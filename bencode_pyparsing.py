"""
This module turned out to be unusable because
bencode format is a binary format but pyparsing only works with unicode.
I am leaving code here because it is a good code example.
"""
from pyparsing import Forward
from pyparsing import Group
from pyparsing import nums
from pyparsing import printables
from pyparsing import StringEnd
from pyparsing import StringStart
from pyparsing import Suppress
from pyparsing import Word
from pyparsing import ZeroOrMore


def to_int_action(toks, idx=0):
    """Convert first token to integer"""
    return int(toks[idx])

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
def strParseAction(s, l, t):
    n = t[0]
    # TODO: we should be able to parse all strings not only printables.
    actualStrParser << Word(printables, exact=n)
    # since we do not need lenght of the parser anymore
    # we can ignore it.
    return []

# strLength parser parses length of the string
# <length of string>:
strLengthParser = Word(nums) + Suppress(':')
strLengthParser.setParseAction(to_int_action)
# after length is parsed create second part of the parser.
strLengthParser.addParseAction(strParseAction, callDuringTry=True)
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
listParser = Group(Suppress('l') + ZeroOrMore(exprParser) + Suppress('e'))


#####################
# Dictionary Parser #
#####################
# Dictionary is formated as
# d[key1][value1][key2][value2][...]e
def dictParseAction(toks):
    """Convert list of key, value tuples to dictionary"""
    return [dict(toks.asList())]

dictParser = (Suppress('d') +
              ZeroOrMore(Group(exprParser + exprParser)) +
              Suppress('e'))
dictParser.setParseAction(dictParseAction)

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
    elif isinstance(obj, (str, unicode)):
        # 'abc' => 3:abc
        resp = '%s:%s' % (len(obj), obj)
    elif isinstance(obj, list):
        # [1, 2, 3] => li1ei2ei3ee
        resp = 'l%se' % ''.join(encode(i) for i in obj)
    elif isinstance(obj, dict):
        # {'key': 'value'} => d3:key5:valuee
        resp = 'd%se' % ''.join(encode(i)
                                for kv in obj.iteritems()
                                for i in kv)
    # TODO: add hadnler for the rest of the types (Exception?)
    return resp

if __name__ == '__main__':
    result = decode('20:12345678901234567890')
    result = decode('i123e')
    result = decode('l1:ai123e2:bce')
    result = decode('l1:ai123e2:bcl1:ai123e2:bcee')
    result = decode('d5:apple3:red6:banana6:yellow5:lemon6:yellow6:violet4:bluee')
    obj = {'key_list': [1, '2', [3], {4: 5}],
           'key_int': 1,
           'key_str': 'a',
           'key_dict': {'a': 'b'}}
    print(encode(obj))
    assert decode(encode(obj)) == obj
    print(result)
