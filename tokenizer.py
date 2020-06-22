import re

def map_match(m):
    filtered_m = {k: m[k] for k in m.groupdict() if m[k] is not None} 
    key, value = next(iter(filtered_m.items()))
    return {"type": key, "value": value}

def tokenize(s, tokens):
    mapped_regex = map(lambda kv: f'(?P<{kv[0]}>{kv[1]})', tokens.items())
    combined = re.compile('|'.join(mapped_regex))
    matches = [map_match(m) for m in re.finditer(combined, s)]
    return matches