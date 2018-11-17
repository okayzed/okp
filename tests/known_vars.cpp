using namespace std;

#include <iostream>
using namespace std;

class A {
public:
    string s;
    auto set_string(auto a) {
        s = a;
        auto r = a; }

    auto shadow_set_string(auto a) {
        // known r;
        r = a; }

    string r; };




int main() {
    A a;

    a.s = "foo";
    auto s = 10;

    a.set_string("bar");
    std::cout << "R" << ' ' << a.r << ' ' << "S" << ' ' << a.s << std::endl;

    a.shadow_set_string("baz");

    std::cout << "R" << ' ' << a.r << ' ' << "S" << ' ' << a.s << std::endl;

    return 0; };


