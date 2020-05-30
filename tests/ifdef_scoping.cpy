def foo():
  abc = 0

$ #ifdef FOO
$ abc
$ #endif

  return abc


def main():
  abc = foo()
