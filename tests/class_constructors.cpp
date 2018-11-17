using namespace std;

#include <iostream>

class MyClass {
    public:
    MyClass() {
        cout << "initializing" << endl; }

    ~MyClass() {
        cout << "destructing" << endl; }

    auto print_stuff() {
        cout << "printing stuff" << endl; } };

int main() {

    MyClass c; };


