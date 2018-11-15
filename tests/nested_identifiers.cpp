
class B {
public:
    int baz; };

class F {
public:
    B bar; };


main() {
    auto foo = F();
    foo.bar.baz = 20;

    auto bar = 10;
    foo = F(); };


