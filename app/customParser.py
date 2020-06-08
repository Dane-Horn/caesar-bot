import re
import random
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
    def getNext(self):
        if self.c != '\0':
            self.i += 1
            self.updateC()
            while(self.c.isspace()):
                self.updateC()
        return self.c

    def parse(self, inpt):
        self.value = 0
        self.c = ''
        self.i = -1
        self.inpt = inpt
        self.output = ''
        self.getNext()
        value = self.expression()
        self.output += f'= {value}'
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
        value = self.factor()
        while self.isMulOp(self.c):
            op = self.c
            self.output += f'{op} '
            self.getNext()
            secondValue = self.factor()
            if op == '*':
                value *= secondValue
            if op == '/':
                value /= secondValue
        return value

    def factor(self):
        if not self.c == 'd' and not self.c == '(' and not (self.isDigit(self.c) or self.c == '-'):
            print('c: ', self.c)
            raise Exception('unexpected end')
        value = None
        if self.c == '(':
            value = self.bracket()
        elif self.isDigit(self.c) or self.c == '-' or self.c == 'd':
            value = self.number()
        return value
    def isAddOp(self, c):
        return c in '+-'

    def isMulOp(self, c):
        return c in '*/'

    def isDigit(self, c):
        return c in '0123456789'

    def number(self):
        if self.c == 'd':
            self.getNext()
            return self.dice(1)
        value = ''
        while self.isDigit(self.c) or self.c == '-':
            value += self.c
            self.getNext()
        self.output += f'{value} '
        if self.c == 'd':
            self.getNext()
            return self.dice(int(value))
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
        if self.c == 'd':
            self.getNext()
            value = self.dice(value)
        return value

    
    def dice(self, num):
        self.output = self.output[:-1]
        self.output += 'd'
        base = self.bracket() if self.c == '(' else self.number()
        self.output = self.output[:-1]
        rolls = [random.randint(1, base) for _ in range(num)]
        value = sum(rolls)
        self.output += '('
        self.output += ' + '.join(map(lambda roll: f'({roll})', rolls))
        self.output += f' = {value}) '
        return value

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