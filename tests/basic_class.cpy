#include <iostream>
#include <tuple>
#include <vector>

using namespace std;

class MyClass:
    public:
        MyClass():
            pass
        ~MyClass():
            pass

        def get_class_str():
          return "Class"


    private:
        def multi_ret():
          return 1, 2

class SecondClass: public MyClass
    public: SecondClass():
        pass

    public: ~SecondClass():
        pass

    public: void mybar():
        pass

    public: string s;

    private: int get_int():
        return 10

def main():
    int i
    int n = 10
    MyClass mc

    vector<int> v(n);
    for i = 0; i < v.size(); i++
      puts v[i]

    print ""


    print mc.get_class_str()
