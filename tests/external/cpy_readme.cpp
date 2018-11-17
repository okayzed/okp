using namespace std;

#include <iostream>
#include <tuple>

using namespace std;

auto operations(int a, int b) {
    auto sum = a + b;
    auto subtract = a - b;
    auto multiply = a * b;
    auto divide = a / b;
    return make_tuple(sum,  subtract,  multiply,  divide); };

int main() {
    auto structuredArgs_0 = operations(20, 10);
    auto sum = get<0>(structuredArgs_0);
    auto mult = get<2>(structuredArgs_0);
    std::cout << sum << ' ' << mult << std::endl; };








