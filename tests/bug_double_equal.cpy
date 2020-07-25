#include <string>

struct App:
  string bin

vector<App> APPS = {\
  {.bin = "foo"},\
  {.bin = "bar"},\
  {.bin = "baz"} };

vector<App> BAPPS = vector<App>(%{
  {.bin = "foo"},
  {.bin = "bar"},
  {.bin = "baz"}
})

def main():
  pass
