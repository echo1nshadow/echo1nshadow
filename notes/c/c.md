#### 一些C语言的知识点

1. 结构体字节对齐
```
#include<stdio.h>
#pragma pack(1)
typedef struct
{
    char  test_char;
    float test_float;
    int   test_int;
    char  test_char2;
}TEST_T1;
#pragma pack()

typedef struct
{
    char  test_char;
    float test_float;
    int   test_int;
    char  test_char2;
}TEST_T2;


typedef struct
{
    char  test_char;
    float test_float;
    int   test_int;
    char  test_char2;
}TEST_T3;

typedef struct
{
    char  test_char;
    char  test_char2;
    float test_float;
    int   test_int;
}TEST_T4;
int main()
{
    printf("sizeof(TEST_T1):%d\n",sizeof(TEST_T1));
    printf("sizeof(TEST_T2):%d\n",sizeof(TEST_T2));
    printf("sizeof(TEST_T3):%d\n",sizeof(TEST_T3));
    printf("sizeof(TEST_T4):%d\n",sizeof(TEST_T4));
    return 0;
}
```

结果:
```
sizeof(TEST_T1):10
sizeof(TEST_T2):16
sizeof(TEST_T3):16
sizeof(TEST_T4):12
```

2. 字节不对齐时直接使用浮点数赋值会导致程序崩溃, 应使用memcpy
3. 