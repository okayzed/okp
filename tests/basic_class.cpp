#include <iostream>
#include <tuple>
#include <vector>

using namespace std;

class AClass {
  public:
      AClass() {
          (void)0; }
      ~AClass() {
          (void)0; } };

class BClass: AClass {
public:
    BClass() {
        (void)0; }
    ~BClass() {
        (void)0; }

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

    public: void mybar() {
        (void)0; }

    public: string s;

    private: int get_int() {
        return 10; } };

main() {
    int i;
    int n = 10;
    CClass mc;

    vector<int> v(n);
    for (i = 0; i < v.size(); i++) {
      std::cout << v[i]; }

    std::cout << "" << std::endl;


    std::cout << mc.get_class_str() << std::endl; };

