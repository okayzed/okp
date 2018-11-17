using namespace std;

#include <iostream>
#include <vector>

#define False false
#define True true
using namespace std;

auto my_function(vector<int> &nums) {
    auto p = True;
    while (p) {
        for (auto i = 0; i < nums.size()-1; i++) {
            if (nums[i] > nums[i + 1]) {
                auto a = nums[i];
                nums[i] = nums[i + 1];
                nums[i + 1] = a;
                p = True; } }

        if (not p) {
            break; }

        p = False;
        for (auto i = nums.size() - 2; i > 0; i--) {
            if (nums[i] > nums[i + 1]) {
                auto q = nums[i+1];
                nums[i+1] = nums[i];
                nums[i] = q;
                p = True; } } }

    return nums; };


int main() {
    vector<int> nums = {1, 3, 4, 100, 2, 9, -1};
    my_function(nums);

    for (auto i : nums) {
        std::cout << i << " "; }
    std::cout << "" << std::endl; };


