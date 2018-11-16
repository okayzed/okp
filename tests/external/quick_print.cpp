
#include <iostream>
#include <string>
int main() {
    int a, b;
    std::string str;
    std::cout << "Type two integers: " ; std::cin >> a >> b ; std::cout << "Well done! Now type a string: " ; std::cin >> str ; std::cout << "Congratulations!\n" ;

    std::cout << std::endl;
    std::cout << "Following line is produced by command: ! a b str \"Second << ' ' << string\"" << std::endl;
    std::cout << a << ' ' << b << ' ' << str << ' ' << "Second string" << std::endl;
    std::cout << std::endl;

    std::cout << "!! is a quick print without ending the line..." << " ";
    std::cout << " Ending the line in the following command exemplified!" << std::endl;

    std::cout << "Following line is produced by command: ?? a b str" << std::endl;
    std::cin >> a >> b >> str ;


    std::cout << "A is valued " << ' ' << a << ' ' << std::endl << std::endl;
    std::cout << "B is valued " << b << std::endl; };

