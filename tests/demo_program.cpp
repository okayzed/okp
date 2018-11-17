
#include <iostream>
#include <tuple>

using namespace std;



class MyClass {
  public:
    string s;
    MyClass() {
        std::cout << "instantiated new class mc" << std::endl; }

    ~MyClass() {
        std::cout << "destructor for mc called" << ' ' << s << std::endl; }

    auto set_string(auto a) {
        s = a; }

    auto get_string() {
        return s; } };



auto foo() {
    std::cout << "test function" << std::endl;
    return make_tuple(1,  2); };

int main() {
    std::cout << "foobar" << std::endl;

    string s;
    std::cin >> s ;
    std::cout << "READ" << ' ' << s << std::endl;

    MyClass mc;
    mc.set_string(s);

    auto structuredArgs_0 = foo();
    auto a = get<0>(structuredArgs_0);
    auto b = get<1>(structuredArgs_0);

    std::cout << a << ' ' << b << std::endl;

    if (true) {
        std::cout << "true" << std::endl; }

    if (not false) {
        std::cout << "false" << std::endl; }

    for (auto i = 0; i < 10; i++) {
      std::cout << "I IS" << ' ' << i << std::endl; }

    return 0; };


