import clang.cindex

s = '''
'''

TokenKind = clang.cindex.TokenKind
idx = clang.cindex.Index.create()

def parse_line(line):
    tu = idx.parse('tmp.cpp', args=['-std=c++11'],
                    unsaved_files=[('tmp.cpp', line)],  options=0)
    for t in tu.get_tokens(extent=tu.cursor.extent):
        yield t


# we do some touchups to remove something like foo.bar.baz
# into only foo
def add_identifiers(line, scope):
    toks = parse_line(line)
    new = []

    new_toks = []
    toks = list(toks)
    while toks:
        t = toks.pop()
        new_toks.append(t)

        if toks:
            nt = toks[-1]
            if nt.spelling == '.' or nt.spelling == '->':
                toks.pop()
                new_toks.pop()


    for t in new_toks:
        if t.kind == TokenKind.IDENTIFIER:
            if t.spelling not in scope:
                new.append(t.spelling)
                scope[t.spelling] = 1

    return new

if __name__ == "__main__":
    scope = {}
    add_identifiers("vector<int> n", scope)
    add_identifiers("foo.bar. baz", scope)
    print scope
