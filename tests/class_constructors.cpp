
#include <iostream>

class MyClass {
    public:
    MyClass() {
        std::cout << "initializing" << std::endl; }

    ~MyClass() {
        std::cout << "destructing" << std::endl; }

    auto print_stuff() {
        std::cout << "printing stuff" << std::endl; } };

int main() {

    MyClass c; };


