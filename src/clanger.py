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

def add_identifiers(line, scope):
    toks = parse_line(line)
    new = []
    for t in toks:
        print t.spelling
        if t.kind == TokenKind.IDENTIFIER:
            if t.spelling not in scope:
                new.append(t.spelling)
                scope[t.spelling] = 1

    return new

if __name__ == "__main__":
    scope = {}
    add_identifiers("vector<int> n", scope)
    add_identifiers("foobar. baz", scope)
    print scope
