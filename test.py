from customParser import Parser
import sys
parser = Parser()

result = parser.parse('2d(d10*2)+2')
print(result)