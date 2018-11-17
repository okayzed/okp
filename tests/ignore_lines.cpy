// test that we dont add semicolon to end of template line
;template<typename T>
def my_func():
    return 0

// we add trailing semi-colons to end of class declaration
// and lines missing
; class MyClass {
;   public:
;       MyClass() {}
; }


def foo_func():
    return rand() % 10

// TODO: spot when the indentation is inconsistent: aka, when we have
// 4 spaces on one line, then 2 on the next
def main():
    int i

  ; for (i = 0; i < 10; i++) {
  ;   cout << foo_func() << endl;
  ; }
  ; cout << endl;

    for i = 0; i < 10; i++:
      puts i
    print
