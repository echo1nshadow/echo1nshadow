#include "test.h"
#include <iostream>
int CTest::get_test1(void)
{
  return test1;
}

CTest::CTest()
{
  std::cout << "CTest constructor\n";
}

CTest::CTest(int _test1, int _test2)
{
  test1 = _test1;
  test2 = _test2;
  std::cout << "CT constructor no argv\n";
}

CTest::~CTest()
{
  std::cout << "CT destructor\n";
}

int CTest2::get_test3()
{
  test3 = test1 + test2;
  std::cout << test3;
  return test3;
}


CTest2::CTest2()
{
  std::cout << "CTest2 constructor no argv\n";
}
CTest2::CTest2(int _argv1, int _argv2)
{
  test1 = _argv1;
  test2 = _argv2;
  std::cout << "CTest2 constructor\n";
}

CTest2::~CTest2()
{
  std::cout << "CTest2 destructor\n";
}