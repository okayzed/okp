namespace foo:
  string bar = "hello"

  int my_func_a():
    pass

  class baz:
    public: 
    int a,b,c
    baz():
      a = 1

  class caz:
    caz():
      pass

  int my_func_b():
    pass

  
int main():
  print "IN MAIN", foo::bar
  b = foo::baz()
