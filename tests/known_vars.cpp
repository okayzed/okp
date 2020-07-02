
#include <iostream>
using namespace std;

class A {
public:
    string s;
    auto set_string(auto a) {
        s = a;
        auto r = a; }

    auto shadow_set_string(auto a) {
        r;
        r = a; }

    string r; };




int main() {
    A a;

    a.s = "foo";
    auto s = 10;

    a.set_string("bar");
    cout << "R" << ' ' <<  a.r << ' ' <<  "S" << ' ' <<  a.s << endl;

    a.shadow_set_string("baz");

    cout << "R" << ' ' <<  a.r << ' ' <<  "S" << ' ' <<  a.s << endl;

    return 0; };



