#### 一些C语言的知识点

- 结构体字节对齐
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

- 字节不对齐时直接使用浮点数赋值会导致程序崩溃, 应使用memcpy

- const的指针和引用
  - 指针
    - 指向常量的指针
    - 自身是常量的指针
    - 指向常量切自身也是常量的指针
  - 引用
    - 指向常量的引用
  ```
  void function()
  {
      // 对象
      A b;                        // 普通对象,可以调用全部成员函数
      const A a;                  // 常对象,只能调用常成员函数
      const A *p = &a;            // 指针变量,指向常对象
      const A &q = a;             // 指向常对象的引用

      // 指针
      char greeting[] = "Hello";
      char* p1 = greeting;                // 指针变量,指向字符数组变量
      const char* p2 = greeting;          // 指针变量,指向字符数组常量（const 后面是 char,说明指向的字符（char）不可改变）
      char* const p3 = greeting;          // 自身是常量的指针,指向字符数组变量（const 后面是 p3,说明 p3 指针自身不可改变）
      const char* const p4 = greeting;    // 自身是常量的指针,指向字符数组常量
  } 
  ```

- inline 内联函数
  - 特征
    - 相当于把内联函数里面的内容写在调用内联函数处 
    - 相当于不用执行进入函数的步骤,直接执行函数体
    - 相当于宏,却比宏多了类型检查,真正具有函数特性
    - 编译器一般不内联包含循环、递归、switch 等复杂操作的内联函数；
    - 在类声明中定义的函数,除了虚函数的其他函数都会自动隐式地当成内联函数
  - 编译器对 inline 函数的处理步骤
    1. 将 inline 函数体复制到 inline 函数调用点处；
    2. 为所用 inline 函数中的局部变量分配内存空间
    3. 将 inline 函数的的输入参数和返回值映射到调用方法的局部变量空间中
    4. 如果 inline 函数有多个返回点,将其转变为 inline 函数代码块末尾的分支（使用 GOTO）
  - 优缺点
    - 优点
      - 内联函数同宏函数一样将在被调用处进行代码展开,省去了参数压栈、栈帧开辟与回收,结果返回等,从而提高程序运行速度
      - 内联函数相比宏函数来说,在代码展开时,会做安全检查或自动类型转换（同普通函数）,而宏定义则不会
      - 在类中声明同时定义的成员函数,自动转化为内联函数,因此内联函数可以访问类的成员变量,宏定义则不能
      - 内联函数在运行时可调试,而宏定义不可以
    - 缺点
      - 代码膨胀。内联是以代码膨胀（复制）为代价,消除函数调用带来的开销。如果执行函数体内代码的时间,相比于函数调用的开销较大,那么效率的收获会很少。另一方面,每一处内联函数的调用都要复制代码,将使程序的总代码量增大,消耗更多的内存空间
      - inline 函数无法随着函数库升级而升级。inline函数的改变需要重新编译,不像 non-inline 可以直接链接(**这个不理解**)
      - 是否内联,程序员不可控。内联函数只是对编译器的建议,是否对函数内联,决定权在于编译器

- 位域 (todo)

