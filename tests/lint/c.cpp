void func(int z) { }
void func(int x, int y) { }

class A {
  int a;
  int b;
  int c;

  int foo() {
    a++;
    func(b);
    b -= 1;

    func(a, b);

    this->c = 3;

    return 3;
  }
};


int main() {
  A a;
  return 0;
}
