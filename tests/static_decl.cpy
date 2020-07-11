class A:
  public:
  static int b

  A():
    A::b = 1

int A::b = 0


def main():
  print "A::B is", A::b
  A()
  print "A::B is", A::b
