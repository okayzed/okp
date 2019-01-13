
#include <iostream>
#include <tuple>

using namespace std;



class MyClass {
  public:
    string s;
    MyClass() {
        cout << "instantiated new class mc" << endl; }

    ~MyClass() {
        cout << "destructor for mc called" << ' ' <<  s << endl; }

    auto set_string(auto a) {
        s = a; }

    auto get_string() {
        return s; } };



auto foo() {
    cout << "test function" << endl;
    return make_tuple(1,  2); };

int main() {
    cout << "foobar" << endl;

    string s;
    cin >> s;
    cout << "READ" << ' ' <<  s << endl;

    MyClass mc;
    mc.set_string(s);

    auto structuredArgs_0 = foo();
    auto a = get<0>(structuredArgs_0);
    auto b = get<1>(structuredArgs_0);

    cout << a << ' ' <<  b << endl;

    if (true) {
        cout << "true" << endl; }

    if (not false) {
        cout << "false" << endl; }

    for (auto i = 0; i < 10; i++) {
      cout << "I IS" << ' ' <<  i << endl; }

    return 0; };


