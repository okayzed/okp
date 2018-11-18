#include <iostream>



#include <map>

using namespace std;


int main() {
    int x, n, d;
    multimap<int, int> q;

    cin >> x n ;

    for (auto i = 0; i < n; i++) {
        cin >> d ;
        q.insert({d, d}); }

    int l, r;

    auto i = 0;
    auto total = 0;


    while (q.size() > 1) {

        l = q.begin();
        auto lv = l->first;
        q.erase(l);
        r = q.begin();
        auto rv = r->first;
        q.erase(r);

        int v = lv + rv;
        total += v;

        q.insert({v, i}); }

    cout << total << endl; };


