#include<iostream>
#include <limits>

using namespace std;  

#include "test.h"
int main(int argc, char** argv)
{
  CTest obj(1,2);
  cout << obj.get_test1() << endl;
  CTest2 obj2(3,4);
  obj2.get_test3();
  return 0;
}
