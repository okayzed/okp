// C++ program to demonstrate implementation 
// of Inheritance 
#include <iostream>

using namespace std 
  
//Base class 
class Parent:
    public: 
      int id_p 
   
// Sub class inheriting from Base Class(Parent) 
class Child : public Parent 
    public: 
      int id_c 
  
//main function 
def main():
    Child obj1 

    // An object of class child has all data members 
    // and member functions of class parent 
    obj1.id_c = 7 
    obj1.id_p = 91 

    print "Child id is " obj1.id_c
    print "Parent id is " obj1.id_p

    return 0 
