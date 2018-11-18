
#include <iostream>
#include <tuple>
#include <vector>

using namespace std;

class AClass {
    public: AClass() {
          (void)0; }
    public: ~AClass() {
          (void)0; } };

class BClass: AClass {
    public: BClass() {
        (void)0; }
    public: ~BClass() {
        (void)0; }

    public:
    auto get_class_str() {
      return "Class"; }

private:
    auto multi_ret() {
      return make_tuple(1,  2); } };

class CClass: public BClass {
    public: CClass() {
        (void)0; }

    public: ~CClass() {
        (void)0; }

    public:
    void mybar() {
        (void)0; }

    string s;

    private: int get_int() {
        return 10; } };

int main() {
    int i;
    int n = 10;
    CClass mc;

    vector<int> v(n);
    for (i = 0; i < v.size(); i++) {
      cout << v[i] << " "; }

    cout << endl;
    cout << mc.get_class_str() << endl; };


