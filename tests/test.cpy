#include <iostream>
#include <tuple>

using namespace std

/*
   ignore
   multi line comments
   please
*/

class MyClass:
    public:
        MyClass():
            print "instantiated new class mc"

        ~MyClass():
            print "destructor for mc called" s

        string s;

        def set_string(auto a):
            s = a

        def get_string():
            return s

    string q

// should auto prepare a tuple when returning multiple
def foo():
    print "test function"
    return 1, 2

def main():
    print "foobar"

    string s
    read s // strip comments
    print "READ" s

    MyClass mc
    mc.set_string(s)

    int a, b
    a, b = foo() // std:tie when assigning from multi

    print a b
    if true:
        print "true"

    if not false:
        print "false"

    return 0
