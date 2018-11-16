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
    string s;
    MyClass():
        print "instantiated new class mc"

    ~MyClass():
        print "destructor for mc called" s

    def set_string(auto a):
        s = a

    def get_string():
        return s


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

    a, b = foo() // std:tie when assigning from multi

    print a b

    if true:
        print "true"

    if not false:
        print "false"

    for i = 0; i < 10; i++:
      print "I IS" i

    return 0
