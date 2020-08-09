// tests/lint/b.cpy
#include <stdlib.h>

using namespace std;

class A {
  int *a;
  int *b;
  string c;
  int *d;
  int *fbmem;


  void draw_pixel(int x, int y, int color) {
    *b = 10;

    auto ptr = this->fbmem;
    ptr[y * (*this->b) + x] = color;

    a = (int*) malloc(1);
    c = 20; } };


int main() {
  (void)0; };


