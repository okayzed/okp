#include <iostream>
#include <vector>

#define False false
#define True true
using namespace std;

def my_function(vector<int> &nums):
    p = True
    while p:
        for i = 0; i < nums.size()-1; i++
            if nums[i] > nums[i + 1]:
                a = nums[i]
                nums[i] = nums[i + 1]
                nums[i + 1] = a
                p = True

        if not p:
            break

        p = False
        for i = nums.size() - 2; i > 0; i--
            if nums[i] > nums[i + 1]:
                q = nums[i+1]
                nums[i+1] = nums[i]
                nums[i] = q
                p = True

    return nums


def main():
    vector<int> nums = {1, 3, 4, 100, 2, 9, -1}
    my_function(nums)

    for auto i : nums:
        puts i " "
    print ""
