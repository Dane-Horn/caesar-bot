import re
import random
from tokenizer import tokenize
class tokenParser():
    def expect(self, *types):
        not_found = all(self.curr.get(token_type, None) is None for token_type in types)
        if not_found:
            raise Exception(f'One of {types} expected, but {self.curr} found')
        return True

    def is_curr(self, *types):
        return any(self.curr.get(token_type, None) is not None for token_type in types)
    def next(self):
        self.i += 1

    @property
    def curr(self):
        if self.i >= len(self.tokens):
            return {'eof': '\0'}
        else:
            return self.tokens[self.i]

    @property
    def curr_value(self):
        if self.i >= len(self.tokens):
            return '\0'
        else:
            return next(iter(self.tokens[self.i].values()))
    def parse(self, s):
        self.i = 0
        self.tokens = tokenize(s)

class Parser():
    inpt = None
    c = ''
    i = 0
    output = ''

    def updateC(self):
        if self.i < len(self.inpt):
            self.c = self.inpt[self.i]
        else:
            self.c = '\0'
    def getNext(self, i=1):
        if self.c != '\0':
            self.i += 1
            self.updateC()
            while(self.c.isspace()):
                self.updateC()
        return self.c
    
    def expect(self, char):
        if self.c != char:
            raise Exception(f'{char} expected')

    def parse(self, inpt):
        self.value = 0
        self.c = ''
        self.i = -1
        self.inpt = inpt
        self.output = ''
        self.getNext()
        value = self.expression()
        self.output += f'= {value}'
        if len(self.output) > 2000:
            self.output = f'...output too long - truncated result = {value}'
        return self.output

    def expression(self):
        value = self.term()
        while self.isAddOp(self.c):
            op = self.c
            self.output += f'{op} '
            self.getNext()
            secondValue = self.term()
            if op == '+':
                value += secondValue
            if op == '-':
                value -= secondValue
        return value 

    def term(self):
        value = self.term2()
        while self.isMulOp(self.c):
            op = self.c
            self.output += f'{op} '
            self.getNext()
            secondValue = self.term2()
            if op == '*':
                value *= secondValue
            if op == '/':
                value /= secondValue
        return value
    
    def term2(self):
        value = None
        if self.match(r'adv'):
            self.output += 'adv'
            self.getNext(); self.getNext(); self.getNext()
            self.expect('(')
            self.getNext()
            self.output += '('
            num_rolls = self.term3()
            self.expect(',')
            self.getNext()
            self.output += ', '
            base = self.term3()
            self.expect(')')
            self.getNext()
            self.output = self.output[:-1]
            self.output += ') '
            rolls, rolls_output = self.dice(num_rolls, base)
            value = max(rolls)
            self.output += f'({", ".join(rolls_output)} = {value}) '
        elif self.match(r'dis'):
            self.output += 'dis'
            self.getNext(); self.getNext(); self.getNext()
            self.expect('(')
            self.getNext()
            self.output += '('
            num_rolls = self.term3()
            self.expect(',')
            self.getNext()
            self.output += ', '
            base = self.term3()
            self.expect(')')
            self.getNext()
            self.output = self.output[:-1]
            self.output += ') '
            rolls, rolls_output = self.dice(num_rolls, base)
            value = min(rolls)
            self.output += f'({", ".join(rolls_output)} = {value}) '
        else:
            value = self.term3()
        return value
    
    def term3(self):
        value = 1
        hasN = False
        if (self.c != 'd'):
            hasN = True
            value = self.factor()
        if self.c == 'd':
            if hasN:
                self.output = self.output[:-1]
            self.output += 'd'
            self.getNext()
            base = self.factor()
            rolls, rolls_output = self.dice(value, base)
            value = sum(rolls)
            self.output += f'({" + ".join(list(rolls_output))} = {value}) '
        return value

    def factor(self):
        if not self.c == '(' and not (self.isDigit(self.c) or self.c == '-'):
            print('c: ', self.c)
            raise Exception('unexpected end')
        value = None
        if self.c == '(':
            value = self.bracket()
        elif self.isDigit(self.c) or self.c == '-':
            value = self.number()
        return value
    def isAddOp(self, c):
        return c in '+-'

    def isMulOp(self, c):
        return c in '*/'

    def isDigit(self, c):
        return c in '0123456789'

    def number(self):
        value = ''
        while self.isDigit(self.c) or self.c == '-':
            value += self.c
            self.getNext()
        self.output += f'{value} '
        if value == '-':
            raise Exception('digit expected')
        return int(value)

    def bracket(self):
        self.output += '('
        self.getNext()
        value = self.expression()
        if self.c != ')':
            raise Exception(') expected')
        self.output = self.output[:-1] + ') '
        self.getNext()
        return value

    
    def dice(self, num, base):
        rolls = [random.randint(1, base) for _ in range(num)]

        rolls_output = iter(["(...)"])
        if len(rolls) < 100:
            rolls_output = map(lambda roll: f'({roll})', rolls)
        return (rolls, rolls_output)

    def removeNumberFromDisplay(self):
        toRemove = 0
        output = self.output[::-1]
        for c in output:
            if not self.isDigit(c):
                break
            toRemove += 1
        self.output = self.output[:-toRemove]
    def removeBracketFromDisplay(self):
        toRemove = 0
        output = self.output[::-1]
        count = 0
        for c in output:
            toRemove += 1
            if c == ')': count += 1
            if c == '(': count -= 1
            if count == 0: break
        self.output = self.output[:-toRemove]
    
    def match(self, pattern):
        if re.match(pattern, self.inpt[self.i:]):
            return True
        return False