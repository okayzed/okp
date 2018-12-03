#include <cmath>

class Sieve:
    vector<int> values
    int last_max

public:
    Sieve():
        // 0 is prime, 1 is prime, 2 is prime, 3 is prime
        // the rest follow from that
        values = { 0, 0, 0, 0 }
        self.last_max = 3

    def resize(int n)
    def make_sieve(int n)
    def is_prime(int n)


def Sieve::resize(int n):
    s = self.values.size()
    while n >= s:
        s <<= 1

    self.values.resize(s+1)
    return s

def Sieve::make_sieve(int n):
    // we don't want to continually re-build our sieve,
    // so we rebuild in powers of 2
    n = self.resize(n)
    m = ceil(sqrt(n))

    for i = 2; i <= m; i++:
        if self.values[i]: // values[i] is not prime if true
            continue

        lm = max(self.last_max / i+1, 2)

        for j = lm; j * i <= n; j++:
            self.values[j*i] = 1

    self.last_max = n

def Sieve::is_prime(int n):
    if self.values.size() <= n:
        self.make_sieve(n)


    return self.values[n] == 0

def is_prime(int n):
    for i = 2; i < n; i++:
        if n % i == 0:
            return false

    return true

int main():
    s = Sieve()
    m = 1000
    all_good = true
    for k = 0; k < m; k++:
        if is_prime(k) != s.is_prime(k):
            print k, s.is_prime(k), is_prime(k)
            all_good = false

    if all_good:
        print "ALL GOOD!"
    else:
        print "A PROBLEM WAS FOUND"
