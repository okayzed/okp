#include <iostream>
#include <vector>
using namespace std;

#include <cmath>

class Sieve {
    vector<int> values;
    int last_max;

public:
    Sieve() {


        values = { 0, 0, 0, 0 };
        this->last_max = 3; }

    auto resize(int n);
    auto make_sieve(int n);
    auto is_prime(int n); };


auto Sieve::resize(int n) {
    auto s = this->values.size();
    while (n >= s) {
        s <<= 1; }

    this->values.resize(s+1);
    return s; };

auto Sieve::make_sieve(int n) {


    n = this->resize(n);
    auto m = ceil(sqrt(n));

    for (auto i = 2; i <= m; i++) {
        if (this->values[i]) {
            continue; }

        auto lm = max(last_max / i+1, 2);

        for (auto j = lm; j * i <= n; j++) {
            this->values[j*i] = 1; } }

    auto last_max = n; };

auto Sieve::is_prime(int n) {
    if (this->values.size() <= n) {
        this->make_sieve(n); }


    return this->values[n] == 0; };

auto is_prime(int n) {
    for (auto i = 2; i < n; i++) {
        if (n % i == 0) {
            return false; } }

    return true; };

int main() {
    auto s = Sieve();
    auto m = 1000;
    auto all_good = true;
    for (auto k = 0; k < m; k++) {
        if (is_prime(k) != s.is_prime(k)) {
            cout << k << ' ' <<  s.is_prime(k) << ' ' <<  is_prime(k) << endl;
            all_good = false; } }

    if (all_good) {
        cout << "ALL GOOD!" << endl; }
    else {
        cout << "A PROBLEM WAS FOUND" << endl; }; };


