#include <iostream>
using namespace std;

class Foo {
public:
    auto barbaz(); };


auto Foo::barbaz() {
    cout << "bar baz" << endl; };


int main() {
    auto f = Foo();
    f.barbaz(); };



