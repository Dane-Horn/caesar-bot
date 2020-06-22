import re

default_tokens = {
    "number": r'\d+',
    "add_op": r'\+|-',
    "mul_op": r'\*|/',
    "variable": r'\$[a-zA-Z]+',
    "function": r'dis|adv',
    "die": r'd',
    "paren": r'\(|\)',
    "comma": r',',
    "unknown": r'.+'
}

def tokenize(s, tokens=default_tokens):
    mapped_regex = map(lambda kv: f'(?P<{kv[0]}>{kv[1]})', tokens.items())
    combined = re.compile('|'.join(mapped_regex))
    matches = [{k: m[k] for k in m.groupdict() if m[k] is not None} for m in re.finditer(combined, s)]
    return matches