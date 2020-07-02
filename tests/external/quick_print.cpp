using namespace std;

#include <iostream>
#include <string>
int main() {
    int a, b;
    std::string str;
    cout << "Type two integers: " ; cin >> a >> b ; cout << "Well done! Now type a string: " ; cin >> str ; cout << "Congratulations!\n" ;

    cout << endl;
    cout << "Following line is produced by command: ! a b str \"Second << ' ' << string\"" << endl;
    cout << a << ' ' << b << ' ' << str << ' ' << "Second string" << endl;
    cout << endl;

    cout << "!! is a quick print without ending the line..." << " ";
    cout << " Ending the line in the following command exemplified!" << endl;

    cout << "Following line is produced by command: ?? a b str" << endl;
    cin >> a >> b >> str;


    cout << "A is valued " << ' ' << a << ' ' << std::endl << endl;
    std::cout << "B is valued " << b << std::endl; };


