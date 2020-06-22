from tokenizer import tokenize

def expect(state, *types):
        not_found = all(curr(state).get(token_type, None) is None for token_type in types)
        if not_found:
            raise Exception(f'One of {types} expected, but {curr} found')
        return True

def is_curr(state, *types):
    return any(curr(state).get(token_type, None) is not None for token_type in types)
def next(state):
    state["i"] += 1

def curr(state):
    if state["i"] >= len(state["tokens"]):
        return {'eof': '\0'}
    else:
        return state["tokens"][state["i"]]

def curr_value(state):
    if state.i >= len(state["tokens"]):
        return '\0'
    else:
        return next(iter(state["tokens"][state["i"]].values()))
def parse(s):
    state = {
        "i": 0,
        "tokens": tokenize(s),
        "output": ""
    }