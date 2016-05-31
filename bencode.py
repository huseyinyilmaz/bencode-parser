from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    ZeroOrMore,Forward,nums,alphas,Suppress,printables


# general parsers for all expressions
exprParser = Forward()

# str parser
ActualStrParser = Forward()


def strParseAction(s, l, t):
    n = t[0]
    ActualStrParser << Word(printables, exact=n)
    return []

strLengthParser = Word(nums) + Suppress(':')
strLengthParser.setParseAction(lambda t: int(t[0]))
strLengthParser.addParseAction(strParseAction, callDuringTry=True)
strParser = strLengthParser + ActualStrParser

# Int Parser
intParser = Suppress('i') + Word(nums) + Suppress('e')
intParser.setParseAction(lambda t: int(t[0]))

# list Parser
listParser = Suppress('l') + ZeroOrMore(exprParser) + Suppress('e')


exprParser << (intParser | strParser | listParser)


if __name__ == '__main__':
    result = exprParser.parseString('10:12345678901234567890')
    result = exprParser.parseString('i123e')
    result = exprParser.parseString('l1:ai123e2:bce')
    print(result)
