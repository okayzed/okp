#include <iostream>
using namespace std;


 template<typename T>
auto my_func() {
    return 0; };



  class MyClass {
    public:
        MyClass() {};
  };

  int foo() {
    cout << "this function should have minimal processing done on it" << endl;
  };

  int foobar() {
    return 0;
  };




class MyClass2 {
  int a, b, c;



};


auto foo_func() {
    return rand() % 10; };



int main() {
    int i;

    for (i = 0; i < 10; i++) {
      cout << foo_func() << endl;
    };
    cout << endl;

    for (i = 0; i < 10; i++) {
      cout << i; }
    cout << endl;

    if (false) return 1;

    return 0; };


