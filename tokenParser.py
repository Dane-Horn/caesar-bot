from tokenizer import tokenize

def expect(state, types):
    found = curr_type(state) in types
    if not found:
        raise Exception(f'One of {types} expected, but {curr(state)} found')
    return True

def is_curr(state, types):
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

def parse(s):
    state = {
        "i": 0,
        "tokens": tokenize(s),
        "output": ""
    }
    expression(state)

def expression(state):
    expect(state, {'function', 'paren', 'number', 'variable'})
    pass

def func_term(state):
    expect(state, {'function', 'die', 'paren', 'number', 'variable'})
    pass

def add_term(state):
    expect(state, {'paren', 'die', 'number', 'variable'})
    pass

def mul_term(state):
    expect(state, {'paren', 'die', 'number', 'variable'})
    pass

def die_term(state):
    expect(state, {'paren', 'die', 'number', 'variable'})
    pass

def factor(state):
    expect(state, 'paren', 'number', 'variable')
    pass

# expression = func_term eof
# func_term  = function"("expression")"|add_term
# add_term   = mul_term{add_op mul_term}
# mul_term   = die_term{mul_op die_term}
# die_term   = factor["d"factor]|"d"factor
# factor     = "("expression")"|number|variable

parse('A+2')