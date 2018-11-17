



#include <iostream>
using namespace std;

int main() {
    int n, m;
    string s;
    cin >> n >> m >> s;
    while (m--) {
        int l, r;
        char c, cn;
        cin >> l >> r >> c >> cn;
        l--; r--;
        for (auto i = l; i <= r; i++) {
            if (s[i] == c) {
                s[i] = cn; } } }
    cout << s; };


