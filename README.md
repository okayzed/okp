# okp

okp (pronounced like okapi) is a python script that processes .cpy files and
generates C++ code.

if the following code makes you happy, okp might be for you:

    def weird_multiply(int a, b):
        for i = 0; i < b; i++:
            a *= b
        return a


    def main():
        int a, b
        read a, b

        print "WEIRD MULTIPLIED:", weird_multiply(a, b)

## status

okp is not a good idea for anyone to use, but try it anyways and let me
know what you've built

## installation

    pip install okp

### motivation

i saw vrsperanza's CPY and the light hit me: a language that looks like python
but compiles like C. i decided i want to write programs in it. okp is my
attempt to write a pre-processor like CPY but in python.

## [usage](USAGE.md)

```
# print c++ source
okp -p file.cpy

# compile code
okp file.cpy

# compile multiple cpy files together
okp file1.cpy file2.cpy

# specify the executable file
okp file1.cpy -o ./a.out

# compile and run 
okp file.cpy -r

# compil and run (stdin is passed to the binary) 
okp file.cpy -ri < input.txt

# compile a hybrid project
okp file1.h file2.cpp file3.cpy -o ./a.out
```

## features

### from CPY

Features that okp implements from CPY are:

* indentation based bracketing
* automatic parenthesization of conditionals
* auto variable declarations
* return multiple values from functions
* automatic variable destructuring
* `for` and `rof` loop shorthand (to enable, use `-for` and `-rof` flags)
* `known` keyword
* `#raw` include directive
* disabling auto variable declarations (-ni flag)
* compilation of hybrid projects

Features that are **not** implemented yet:

* export project + Makefile

### original

Some original features of okp to make it look more pythonic are:

* `def` keyword before function names
* `block` keyword for creating blocks
* `pass` keyword for no-ops
* `print` and `raw_input` keywords
* `self` keyword
* lines that start with IGNORE_CHAR are not pre-processed
* triple backticks for multi-line escapes

## further resources and similar projects

* [CPY github](https://github.com/vrsperanza/CPY)
* [what if c looked more like python](http://cpprocks.com/what-if-c-looked-more-like-python-or-coffeescript/)
* [coffee++](https://bixense.com/coffeepp/)
* [MyDef](https://github.com/hzhou/MyDef)
