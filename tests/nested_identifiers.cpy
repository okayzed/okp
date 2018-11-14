class B:
public:
    int baz

class F:
public:
    B bar


def main():
    auto foo = F();
    foo.bar.baz = 20

    bar = 10
    foo = F()
