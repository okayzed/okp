// from http://cpprocks.com/what-if-c-looked-more-like-python-or-coffeescript/

#include <iostream>
using namespace std

namespace utils
    template<typename T>
    auto square(const T& n)
        return n * n

int main()
    auto input = 0
    auto message = "Please enter a positive number"

    cout << message << ":" << endl
    cin >> input

    if input > 0
        cout << "Result: " << utils::square(input) << endl
    else
        cout << message << endl
    return 0
