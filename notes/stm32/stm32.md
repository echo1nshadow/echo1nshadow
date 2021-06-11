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

2. 任务调度
  - 任务调度中的就绪表由两部分组成: ```OSRdyGrp```和```OSRdyTbl[]```
  - 优先级计算
    ```
      这个表本质上是在描述 0x0~0xff 这256个数最低有效位的位置
      INT8U  const  OSUnMapTbl[256] = {
          0u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0x00 to 0x0F                   */
          4u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0x10 to 0x1F                   */
          5u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0x20 to 0x2F                   */
          4u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0x30 to 0x3F                   */
          6u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0x40 to 0x4F                   */
          4u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0x50 to 0x5F                   */
          5u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0x60 to 0x6F                   */
          4u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0x70 to 0x7F                   */
          7u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0x80 to 0x8F                   */
          4u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0x90 to 0x9F                   */
          5u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0xA0 to 0xAF                   */
          4u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0xB0 to 0xBF                   */
          6u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0xC0 to 0xCF                   */
          4u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0xD0 to 0xDF                   */
          5u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, /* 0xE0 to 0xEF                   */
          4u, 0u, 1u, 0u, 2u, 0u, 1u, 0u, 3u, 0u, 1u, 0u, 2u, 0u, 1u, 0u  /* 0xF0 to 0xFF                   */
      };
      y = OSUnMapTbl[OSRdyGrp];-----------(1)
      x = OSUnMapTbl[OSRdyTbl[y]];--------(2)
      prio = (y << 3) + x;----------------(3)
    ```
  - 任务挂起
  - 任务恢复
  - 寻找优先级最高的就绪任务
    ```
      /*
      *********************************************************************************************************
      *                               FIND HIGHEST PRIORITY TASK READY TO RUN
      *
      * Description: This function is called by other uC/OS-II services to determine the highest priority task
      *              that is ready to run.  The global variable 'OSPrioHighRdy' is changed accordingly.
      *
      * Arguments  : none
      *
      * Returns    : none
      *
      * Notes      : 1) This function is INTERNAL to uC/OS-II and your application should not call it.
      *              2) Interrupts are assumed to be disabled when this function is called.
      *********************************************************************************************************
      */

      static  void  OS_SchedNew (void)
      {
          INT8U   y;
          y             = OSUnMapTbl[OSRdyGrp];
          OSPrioHighRdy = (INT8U)((y << 3u) + OSUnMapTbl[OSRdyTbl[y]]);
      }
    ```
    ```OS_SchedNew()``` 函数在三种情况下被调用:
    1. ```OSStart()``` 当系统开始进行任务调度时
    2. ```OSIntExit()``` 当系统执行完最后一个中断函数(ISR)时
    3. ```OS_Sched()``` uCos 本身进行任务调度
    ```OS_SchedNew()```中计算得出的```OSPrioHighRdy```在```OS_CPU_PendSVHandler(void)```中被使用
  - OS_CPU_PendSVHandler()
    ```
    OS_CPU_PendSVHandler:
      CPSID   I                                   @ Prevent interruption during context switch
      MRS     R0, PSP                             @ PSP is process stack pointer
      CBZ     R0, OS_CPU_PendSVHandler_nosave     @ Skip register save the first time

      SUBS    R0, R0, #0x20                       @ Save remaining regs r4-11 on process stack
      STM     R0, {R4-R11}

      LDR     R1, =OSTCBCur                       @ OSTCBCur->OSTCBStkPtr = SP;
      LDR     R1, [R1]                            @echo1nshadow 注: OSTCBCur结构体的第一个成员即为当前任务栈指这里是获取到OSTCBCur的地址后,
                                                   从该地址取第一个32位值出来, 即 R1 为 OSTCBCur->OSTCBStkPtr
      STR     R0, [R1]                            @ R0 is SP of process being switched out

                                                  @ At this point, entire context of process has been saved
    OS_CPU_PendSVHandler_nosave:
      PUSH    {R14}                               @ Save LR exc_return value
      LDR     R0, =OSTaskSwHook                   @ OSTaskSwHook();
      BLX     R0
      POP     {R14}

      LDR     R0, =OSPrioCur                      @ OSPrioCur = OSPrioHighRdy;
      LDR     R1, =OSPrioHighRdy
      LDRB    R2, [R1]
      STRB    R2, [R0]

      LDR     R0, =OSTCBCur                       @ OSTCBCur  = OSTCBHighRdy;
      LDR     R1, =OSTCBHighRdy
      LDR     R2, [R1]
      STR     R2, [R0]

      LDR     R0, [R2]                            @ R0 is new process SP; SP = OSTCBHighRdy->OSTCBStkPtr;
      LDM     R0, {R4-R11}                        @ Restore r4-11 from new process stack
      ADDS    R0, R0, #0x20
      MSR     PSP, R0                             @ Load PSP with new process SP
      ORR     LR, LR, #0xF4                       @ Ensure exception return uses process stack
                                                  @ 进程栈最低两位永远为 0
      CPSIE   I
      BX      LR                                  @ Exception return will restore remaining context
    ```
    注意:
    1. PendSV 是被用来引起一次上下文切换的. 这是 Cortex-M4 推荐的触发上下文切换的方法.
       Cortex-M4 会在进入任何时自动保存一半的上下文环境, 并且会在从异常返回时自动恢复, 所以只需要保存 R4-R11 寄存器以及处理栈指针.
       这样使用 PendSV 意味着不管是在线程中或是在异常、中断中启动, 上下文的保存和恢复是完全一样的.
    2. 伪代码(Pseudo-code)
       1. 获取 PSP 寄存器, 如果为 0 则跳过保存环节, 执行步骤 4
       2. 保存进程栈中的 R4-R11 寄存器
       3. 将进程栈指针保存在它的 TCB 中, OSTCBCur->OSTCBStkPtr = SP
       4. 调用```OSTaskSwHook()```, 这个函数允许你在上下文切换的时候做其他的操作(保存浮点寄存器)
       5. 获取当前最高优先级, OSPrioCur = OSPrioHighRdy
       6. 获取就绪状态线程的 TCB, OSTCBCur = OSTCBHighRdy
       7. 从 TCB 中获取新的 PSP, SP = OSTCBHighRdy->OSTCBStkPtr
       8. 从新的进程栈中恢复 R4-R11
       9. 执行异常返回, 恢复剩余的上下文环境
    3. 当进入 PendSV handler 时:
       1. xPSR, PC, LR, R12, R0-R3 保存到栈中
       2. 处理器模式由线程模式切换到 handler 模式
       3. 栈由进程栈切换到主栈
       4. ```OSTCBCur``` 指向即将被挂起的任务 TCB,
          ``` OSTCBHighRdy``` 指向将被恢复执行的任务 TCB
    4. 由于 PendSv 被系统设置为最低优先级, 我们知道仅当没有其他异常或中断处于活动状态时才会运行, 所以可以假设上下文切换时使用的是进程栈(PSP)

3. uCOS 如何保证实时性
   
#### Cortex-M4常见的汇编
1. 条件标志/更新条件标志
  - 条件标志|置位/清除
   ---    | ---
   N      | 当运算的结果为负数的话置位, 其余情况清0
   Z      | 当运算的结果为 0 的话置位, 其余情况清0
   C      | 当运算的结果产生进位或者减法运算没有借位的话置位, 其余情况清0
   V      | 当运算的结果产生溢出的话置位, 其余情况清0
  - 更新条件标志 S
   条件标志大部分情况下, 不会自动更新到 CPSR 中, 只有指令明确需要更新条件标志才会更新
2. CPSID/CPSIE 快速的开关中断
   CPSID I    @关闭中断 ,  I -- IRQ
   CPSIE I    @打开中断 
   CPSID F    @关闭快速中断 F -- FIQ 快速中断
   CPSIE F    @打开快速中断 
3. CBZ/CBNZ
   ```CBZ Rn, <label>```
   如果 R<sub>n</sub>为 0 则跳转到```<lable>```标号
   ```CBNZ Rn, <label>```
   如果 R<sub>n</sub>不为 0 则跳转到```<lable>```标号
4. SUB
   SUBS R0, R1, R2;   @ R0 = R1 - R2  // SUB**S** 意味着要主动更新条件标志, R1 - R2 没有发生借位则 C 置位, 有则 C 清零
5. MRS/MSR
   MRS: 状态寄存器到通用寄存器的传送指令
   MSR: 通用寄存器到状态寄存器的传送指令
6. LDR/STR
   LDR{条件}  目的寄存器, <存储器地址>
   eg:
      LDR R0，[R1]         ;将存储器地址为R1的字数据读入寄存器R0
   STR{条件}  源寄存器, <存储器地址>
   eg:
      STR R0, [R1],#8      ;将R0中的字数据写入以R1为地址的存储器中,并将新地址R1＋8写入R1
7. STM/LDM
   

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
