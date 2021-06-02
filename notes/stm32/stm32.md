#### stm32cubemx
1. 

#### uCos
1. 内存管理
  - uCos 将存储区域分成**区**和**块**, 每个存储区有数量不等大小相同的存储块, 系统中可存在多个存储区
  - 内存分区、内存块的使用情况由**内存控制块**来记录
    ```
    typedef struct os_mem {           /* MEMORY CONTROL BLOCK                                    */
    void   *OSMemAddr;                /* Pointer to beginning of memory partition                */
    void   *OSMemFreeList;            /* Pointer to list of free memory blocks                   */
    INT32U  OSMemBlkSize;             /* Size (in bytes) of each block of memory                 */
    INT32U  OSMemNBlks;               /* Total number of blocks in this partition                */
    INT32U  OSMemNFree;               /* Number of memory blocks remaining in this partition     */
    #if OS_MEM_NAME_EN > 0u
    INT8U  *OSMemName;                /* Memory partition name                                   */
    #endif
    } OS_MEM;
    ```
    **OSMemAddr**是指向内存分区起始地址的指针, 它在建立内存分区```OSMemCreate()```时被初始化, 此后不能再更改
    **OSMemFreeList**是指向下一个空闲内存控制块或者下一个空闲的内存块的指针
    **OSMemBlkSize**是内存分区中内存块的大小, 是用户建立该内存分区时指定的
    **OSMemNBlks**是内存分区中总的内存块数量, 也是用户建立该内存分区时指定的
    **OSMemNFree**是内存分区中当前可以得空闲内存块数量
  - 使用内存需经过以下步骤:
    1. 建立一个内存分区 OSMemCreate()
    2. 调用OSMemGet()函数从已经建立的内存分区中申请内存块
    3. 当用户应用程序不再使用一个内存块时, 调用OSMemPut()释放内存
    4. 在这过程中可以调用OSMemQuery()查询一个内存分区的状态
  - 内存分区的创建
    ```
      INT8U     *pblk;
      void     **plink

      plink = (void **)addr;                /* Create linked list of free memory blocks      */
      pblk  = (INT8U *)addr;
      loops  = nblks - 1u;
      for (i = 0u; i < loops; i++) 
      {
        pblk +=  blksize;                   /* Point to the FOLLOWING block                  */
       *plink = (void  *)pblk;              /* Save pointer to NEXT block in CURRENT block   */
        plink = (void **)pblk;              /* Position to  NEXT block                  */
      }
      *plink              = (void *)0;      /* Last memory block points to NULL              */
    ```
    addr 是内存分区的起始地址
    plink 是指向void指针的指针
    pblk 用于按 blksize 递增划分区域
    ```*plink = (void  *)pblk;``` 将下一个内存块的地址保存在当前内存块的首地址空间中.

  - 内存的分配与回收
    - OSMemGet()
      ```
        pblk                = pmem->OSMemFreeList;    /* point to next free memory block          */
        pmem->OSMemFreeList = *(void **)pblk;         /* Adjust pointer to new free list          */
        pmem->OSMemNFree--;                           /* One less memory block in this partition  */
      ```
      从pmem中获取空闲的内存块, 并取得这个空闲内存块指向的下一个空闲内存块加入到pmem的链表中, 返回pblk
    - OSMemPut()

#### 电路方面的知识
1. 开漏输出与推挽输出
  - 推挽输出
    推挽输出的最大特点是可以真正能真正的输出高电平和低电平,在两种电平下都具有驱动能力
    **所谓的驱动能力,就是指输出电流的能力**
  - 开漏输出
    开漏输出和推挽输出的区别最普遍的说法就是开漏输出无法真正输出高电平,即高电平时没有驱动能力,需要借助外部上拉电阻完成对外驱动

2. V<sub>S</sub><sub>S</sub>/V<sub>D</sub><sub>D</sub>/V<sub>C</sub><sub>C</sub>
- V<sub>S</sub><sub>S</sub>
  表示公共连接的意思, 通常指电路公共接地端电压
- V<sub>D</sub><sub>D</sub>
  表示器件的意思, 即器件内部的工作电压
- V<sub>C</sub><sub>C</sub>
  表示电路的意思, 即接入电路的电压

3. 三极管

4. 上拉/下拉
  GPIO线路可以有三个状态：
    逻辑低电平(和GND相连)
    逻辑高电平(和VCC相连)
    高阻抗,也称为“悬空”(floating)、高阻(Hi-Z)和三态(tri-stated)
  如果某条线路是高阻抗(High-impedance)状态,那么它实际上就从电路中移除了. 这使得多个电路或设备能够共用输出线路,就可以实现通信总线(communication buses). 在需要高阻抗的场合但没能使用高阻态会导致I/O争用(I/O contention)和短路(short-circuit)
  如果信号的状态不确定,则称为悬空(Floating),表示它没有连接到VCC或GND。该信号的电压会“悬空”,和残余电压匹配
#### stm32基础知识
1. GPIO
- 每个 GPI/O 端口有:
    - 两个 32 位配置寄存器(GPIOx_CRL,GPIOx_CRH)
    - 两个 32 位数据寄存器(GPIOx_IDR(输入),GPIOx_ODR(输出))
    - 一个 32 位置位/复位寄存器(GPIOx_BSRR)
    - 一个 16 位复位寄存器(GPIOx_BRR)
    - 一个 32 位锁定寄存器(GPIOx_LCKR)

- 每个 I/O 端口位可以自由编程,然而 I/0 端口寄存器必须按 32 位字被访问(不允许半字或字节访问)

- GPIO的复用
  复用:作为I2C,SPI,USART等通讯接口

2. 时钟
  - PLL电路(PhaseLockedLoop)
