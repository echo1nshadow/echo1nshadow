#ifndef TEST_H
#define TEST_H

class CTest
{
  public:
    CTest();
    CTest(int, int);
    ~CTest();
    int get_test1(void);
    int test1;
    int test2;

};


class CTest2: public CTest
{
  private:
    int test3;
  public:
    CTest2();
    CTest2(int, int);
    ~CTest2();
    int get_test3();
};
#endif

