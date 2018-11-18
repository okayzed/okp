// this shouldn't compile because l,r are over-written with
// the wrong variable type
#include <map>

using namespace std;


def main():
    int x, n, d
    multimap<int, int> q;

    read x n

    for i = 0; i < n; i++:
        read d
        q.insert({d, d})

    int l, r

    i = 0
    total = 0

    // this should fail because l and r are already declared
    while q.size() > 1:

        l = q.begin()
        lv = l->first
        q.erase(l)
        r = q.begin()
        rv = r->first
        q.erase(r);
        
        int v = lv + rv
        total += v

        q.insert({v, i})

    print total
