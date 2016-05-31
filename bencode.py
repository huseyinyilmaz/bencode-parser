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

if __name__ == '__main__':
    result = decode('20:12345678901234567890')
    result = decode('i123e')
    result = decode('l1:ai123e2:bce')
    result = decode('l1:ai123e2:bcl1:ai123e2:bcee')
    result = decode('d5:apple3:red6:banana6:yellow5:lemon6:yellow6:violet4:bluee')

    print(result)
