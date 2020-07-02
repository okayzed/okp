
auto foo() {
  auto abc = 0;

  #ifdef FOO
  abc
  #endif

  return abc; };


int main() {
  auto abc = foo(); };



