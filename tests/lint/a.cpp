class Foo {
  int foo;
  vector<int> baz;
  Foo() {
    foo = 10;
  }

  void bar() {
    foo = 20;
    bar = 30;
    baz = {};
  }

  void baz() {
    this->foo = 30;
  }

}
