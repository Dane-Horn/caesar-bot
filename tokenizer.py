import re

tokens = {
    "number": r'(?P<number>\d+)',
    "add_op": r'(?P<add_op>\+|-)',
    "mul_op": r'(?P<mul_op>\*|/)',
    "function": r'(?P<function>dis|adv)',
    "die": r'(?P<die>d)',
    "paren": r'(?P<paren>\(|\))',
    "comma": r'(?P<comma>,)',
    "unknown": r'(?P<unknown>.+)'
}


combined = re.compile('|'.join(tokens.values()))
def tokenize(s):
    matches = []
    matches = [{k: m[k] for k in m.groupdict() if m[k] is not None} for m in re.finditer(combined, s)]
    return matches

tokenize('dis+dis2asd')