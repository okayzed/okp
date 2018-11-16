from .util import *

def is_identifier(w):
    if not w:
        return False

    if not w[0].isalpha() and w[0] != '_':
        return False

    if w.replace('_', '').isalnum():
        return True

    return False
        
def find_identifiers(line):
    seps = list(',;.=->*+/()[]%')
    seps.append(' ')
    return smart_split(line, seps, keep_splitters=True)

# we do some touchups to remove something like foo.bar.baz
# into only foo
def add_identifiers(line, scope):
    toks = find_identifiers(line)

    new = []

    new_toks = []
    toks = ['', '']
    toks.extend(list(find_identifiers(line)))
    while toks:
        t = toks.pop()
        new_toks.append(t)

        if toks:
            nt = toks[-1]
            if nt == '.':
                toks.pop()
                new_toks.pop()

            if nt == '>':
                pt = toks[-2]
                if pt == '-':
                    toks.pop()
                    toks.pop()
                    new_toks.pop()
                

    for t in new_toks:
        if is_identifier(t):
            if t not in scope:
                new.append(t)
                scope[t] = 1
    
    return new

if __name__ == "__main__":
    scope = {}
    add_identifiers("node** tree_init()", {})
