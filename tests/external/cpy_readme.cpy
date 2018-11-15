#include <iostream>
#include <tuple>

using namespace std;

operations(int a, b)
	sum = a + b
	subtract = a - b
	multiply = a * b
	divide = a / b
	return sum, subtract, multiply, divide

main()
	sum, _, mult = operations(20, 10)
	! sum mult

// Produces the output:
// 30 200

//_ variables mean ignore this return value
//The last variables can be omitted if not necessary
