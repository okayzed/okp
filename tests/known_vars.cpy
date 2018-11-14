#include <iostream>
using namespace std;

class A:
public:
    string s;
    def set_string(auto a):
        s = a
        r = a

    def shadow_set_string(auto a):
        known r
        r = a

    string r




main():
    A a;

    a.s = "foo"
    s = 10

    a.set_string("bar")
    print "R", a.r, "S", a.s

    a.shadow_set_string("baz")

    print "R", a.r, "S", a.s

    return 0
