# ${NAME}

${NAME} is a python script that processes .cpy files and generates C++ code.

if the following code makes you happy, ${NAME} might be for you:

    #include <iostream>

    def weird_multiply(int a, b):
        for i = 0; i < b; i++:
            a *= b
        return a


    def main():
        int a, b
        read a, b

        print "WEIRD MULTIPLIED:" weird_multiply(a, b)

## status

${NAME} is not a good idea for anyone to use, but try it anyways

## features

### from CPY

Features that ${NAME} implements from CPY are:

* indentation based bracketing
* automatic parenthesization of conditionals
* auto variable declarations
* return multiple values from functions
* automatic variable destructuring
* for loop shorthand
* `known` keyword
* `#raw` include directive

Features that are **not** implemented yet:

* `rof` keyword
* compilation of hybrid projects
* disabling auto variable declarations (-ni flag)

### original

Some original features of ${NAME} to make it look more pythonic are:

* `def` keyword before function names
* `block` keyword for creating blocks
* `pass` keyword for no-ops
* `print` and `read` keywords

### motivation

i saw vrsperanza's CPY and the light was upon me: a language that looks like
python but compiles like C. i decided i want to write programs in it.

${NAME} is an attempt to write a pre-processor like CPY but in python.

## further resources

* [CPY github](https://github.com/vrsperanza/CPY)
* [what if c looked more like python](http://cpprocks.com/what-if-c-looked-more-like-python-or-coffeescript/)
