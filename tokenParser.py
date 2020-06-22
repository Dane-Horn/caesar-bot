from tokenizer import tokenize
from random import randint
add_ops = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b
}

mul_ops = {
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b
}

def disadvantage(state, out, rolls, base):
    rolls = [randint(1, base) for _ in range(rolls)]
    value = min(rolls)
    output(state, out, f'({value})')
    return value
def advantage(state, out, rolls, base):
    rolls = [randint(1, base) for _ in range(rolls)]
    value = max(rolls)
    output(state, out, f'({value})')
    return value
functions = {
    'dis': disadvantage,
    'adv': advantage
}


def expect(state, types):
    found = curr_type(state) in types
    if not found:
        raise Exception(f'One of {types} expected, but {curr(state)} found')
    return True

def match(state, types):
    return curr_type(state) in types

def next_token(state):
    state["i"] += 1

def curr(state):
    if state["i"] >= len(state["tokens"]):
        return {"type": 'eof', "value": '\0'}
    else:
        return state["tokens"][state["i"]]

def curr_type(state):
    return curr(state)["type"]

def curr_value(state):
    return curr(state)["value"]

def output(state, out, *strings):
    if out:
        state["output"].extend(strings)

def parse(s):
    state = {
        "i": 0,
        "tokens": tokenize(s),
        "output": []
    }
    value = expression(state)
    print(value)
    print(state["output"])

# expression = func_term
def expression(state, out=True):
    expect(state, {'function', 'die', 'lparen', 'number', 'variable'})
    value = add_term(state, out)
    return value


# add_term   = mul_term{add_op mul_term}
def add_term(state, out=True):
    expect(state, {'function', 'lparen', 'die', 'number', 'variable'})
    value = mul_term(state, out)
    while match(state, {'add_op'}):
        op = curr_value(state)
        next_token(state)
        second_value = mul_term(state, out)
        value = add_ops[op](value, second_value)
    return value

# mul_term   = die_term{mul_op die_term}
def mul_term(state, out=True):
    expect(state, {'function', 'lparen', 'die', 'number', 'variable'})
    value = die_term(state, out)
    while match(state, {'mul_op'}):
        op = curr_value(state)
        next_token(state)
        second_value = die_term(state, out)
        value = mul_ops[op](value, second_value)
    return value

# die_term   = "d"factor|factor["d"factor]
def die_term(state, out=True):
    value = None
    expect(state, {'function', 'lparen', 'die', 'number', 'variable'})
    if match(state, {'die'}):
        next_token(state)
        base = factor(state, out)
        value = randint(1, base)
    else:
        value = factor(state, out)
        if match(state, {'die'}):
            next_token(state)
            base = factor(state, out)
            value = sum(randint(1, base) for _ in range(value))
    return value

# factor     = "("expression")"|function"("expression{","expression}")"|number|variable
# ignoring variable functionality for now
def factor(state, out=True):
    expect(state, {'function', 'lparen', 'number'})
    if match(state, {'lparen'}):
        next_token(state)
        value = expression(state, out)
        expect(state, {'rparen'})
        next_token(state)
    elif match(state, {'function'}):
        func = curr_value(state)
        next_token(state)
        expect(state, {'lparen'})
        next_token(state)
        args = [state, out]
        args.append(expression(state, out))
        while match(state, {"comma"}):
            next_token(state)
            args.append(expression(state, out))
        value = functions[func](*args)
        expect(state, {'rparen'})
        next_token(state)
    else:
        value = int(curr_value(state))
        next_token(state)
    return value