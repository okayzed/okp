#include <iostream>
#include <tuple>
#include <vector>

using namespace std;

class AClass:
    public: AClass():
          pass
    public: ~AClass():
          pass

class BClass: AClass
    public: BClass():
        pass
    public: ~BClass():
        pass

    public:
    def get_class_str():
      return "Class"

    private:
    def multi_ret():
      return 1, 2

class CClass: public BClass
    public: CClass():
        pass

    public: ~CClass():
        pass

    public:
    def void mybar():
        pass

    string s;

    private: int get_int():
        return 10

def main():
    int i
    int n = 10
    CClass mc

    vector<int> v(n);
    for i = 0; i < v.size(); i++
      puts v[i]

    print
    print mc.get_class_str()
