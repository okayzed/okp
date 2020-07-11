#include <functional>

namespace tq:
  def add_task(std::function<void()> f):
    return


def main():
  tq::add_task([=]() {
    print "TASK WAS ADDED"
  });
