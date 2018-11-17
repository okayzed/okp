
#include <vector>
#include <iostream>

using namespace std;

auto a(int size) {
    vector<int> arr(size);
    for (auto i = 0; i < size; i++) {
        arr[i] = 0; }

    return arr; };


auto b(vector<int> &arr) {
    for (auto i = 0; i < arr.size(); i++) {
        arr[i] = 0; } };

auto c(vector<int> &arr) {
    for (auto i = 0; i < arr.size(); i++) {
        cout << arr[i] << " "; }
    cout << endl; };

int main() {
    auto f = a(10);
    f[0] = 1;
    f[2] = 8;

    c(f);
    b(f);
    c(f); };


