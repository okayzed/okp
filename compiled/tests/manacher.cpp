

#include <bits/stdc++.h>


auto manacher(char *s, int n) {
    std::vector<int> u(n <<= 1, 0);
    for (int i = 0, j = 0,  k; i < n; i += k, j = std::max(j - k, 0)) {
        while (i >= j && i + j + 1 < n && s[(i - j) >> 1] == s[(i + j + 1) >> 1]) {
                        ++j; }
        for (u[i] = j, k = 1; i >= k && u[i] >= k && u[i - k] != u[i] - k; ++k) {
            u[i + k] = std::min(u[i - k], u[i] - k); } }
    return u; };


main() {
    auto s = "babbaa";
    auto u = manacher((char *) s, 10);

    auto mm = 0;
    for (auto m : u) {
      mm = std::max(m, mm); }

    std::cout << mm << std::endl; };


