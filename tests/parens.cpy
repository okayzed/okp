#include <vector>
#include <iostream>

using namespace std;

def a(int size):
    vector<int> arr(size);
    for (i = 0; i < size; i++) 
        arr[i] = 0;

    return arr


def b(vector<int> &arr):
    for i = 0; i < arr.size(); i++:
        arr[i] = 0

def c(vector<int> &arr):
    for(i = 0; i < arr.size(); i++):
        !! arr[i]
    !

def main():
    f = a(10);
    f[0] = 1
    f[2] = 8

    c(f)
    b(f);
    c(f)
