
#include <iostream>
#include <time.h>
#include <tuple>
using namespace std;

auto genArray(int size, int maxVal) {
    auto arr = (int*)malloc(size * sizeof(int));
    for (auto i = 0; i < size; i++) {
        arr[i] = rand()%maxVal; }
    return arr; };

auto findBiggestSmallest(int * arr, int size) {
    auto max = arr[0];
    auto min = arr[0];

    for (auto i = 0; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i]; }

        if (arr[i] < min) {
            min = arr[i]; } }

    return make_tuple(max,  min); };

int main() {
    srand(time(NULL));
    int size, maxVal;
    cout << "Input array size and max value: " ; cin >> size >> maxVal ;

    auto arr = genArray(size, maxVal);

    auto structuredArgs_0 = findBiggestSmallest(arr, size);
    auto max = get<0>(structuredArgs_0);
    auto min = get<1>(structuredArgs_0);

    cout << "Array:" << " ";
    for (auto i = 0; i < size; i++) {
        cout << arr[i] << " "; }
    cout << endl;

    cout << "Biggest number:" << ' ' << max << endl;
    cout << "Smallest number:" << ' ' << min << endl; };

