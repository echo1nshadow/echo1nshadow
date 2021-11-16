#### FreeRTOS笔记

1. 启动任务完成后使用```osThreadSuspend(osThreadGetId())```来挂起任务, 不要使用```osThreadYield()```


##### 内存管理
1. 堆初始化
   ```
    typedef struct A_BLOCK_LINK
    {
        struct A_BLOCK_LINK *pxNextFreeBlock;   // 指向下一个空闲内存块
        size_t xBlockSize;                      // 空闲块的大小
    } BlockLink_t;

    static void prvHeapInit( void )
    {
        BlockLink_t *pxFirstFreeBlock;
        uint8_t *pucAlignedHeap;
        size_t uxAddress;
        size_t xTotalHeapSize = configTOTAL_HEAP_SIZE;

        /* Ensure the heap starts on a correctly aligned boundary. */
        uxAddress = ( size_t ) ucHeap;          // ucHeap 是编译时静态分配的内存块, 大小为 configTOTAL_HEAP_SIZE

        /*  保证字节对齐
            如果ucHeap不是字节对齐的, 那么向上取一个对齐单位的地址, 同时内存总大小相应减小
        */
        if( ( uxAddress & portBYTE_ALIGNMENT_MASK ) != 0 )
        {
            uxAddress += ( portBYTE_ALIGNMENT - 1 );
            uxAddress &= ~( ( size_t ) portBYTE_ALIGNMENT_MASK );
            xTotalHeapSize -= uxAddress - ( size_t ) ucHeap;
        }

        pucAlignedHeap = ( uint8_t * ) uxAddress;           // 对齐后的堆地址

        /* xStart is used to hold a pointer to the first item in the list of free
        blocks.  The void cast is used to prevent compiler warnings. */
        /* xStart 指向第一个可用来分配的空闲链节点 */
        xStart.pxNextFreeBlock = ( void * ) pucAlignedHeap;
        xStart.xBlockSize = ( size_t ) 0;

        /* pxEnd is used to mark the end of the list of free blocks and is inserted
        at the end of the heap space. */
        /* pxEnd 用于标记空闲链末端的位置 */
        uxAddress = ( ( size_t ) pucAlignedHeap ) + xTotalHeapSize;
        uxAddress -= xHeapStructSize;                           // 减去一个链表结构体的大小
        uxAddress &= ~( ( size_t ) portBYTE_ALIGNMENT_MASK );   // 字节对齐
        pxEnd = ( void * ) uxAddress;
        pxEnd->xBlockSize = 0;
        pxEnd->pxNextFreeBlock = NULL;

        /* To start with there is a single free block that is sized to take up the
        entire heap space, minus the space taken by pxEnd. */
        /* 首先, 
        pxFirstFreeBlock = ( void * ) pucAlignedHeap;
        pxFirstFreeBlock->xBlockSize = uxAddress - ( size_t ) pxFirstFreeBlock;
        pxFirstFreeBlock->pxNextFreeBlock = pxEnd;

        /* Only one block exists - and it covers the entire usable heap space. */
        xMinimumEverFreeBytesRemaining = pxFirstFreeBlock->xBlockSize;
        xFreeBytesRemaining = pxFirstFreeBlock->xBlockSize;

        /* Work out the position of the top bit in a size_t variable. */
        xBlockAllocatedBit = ( ( size_t ) 1 ) << ( ( sizeof( size_t ) * heapBITS_PER_BYTE ) - 1 );
    }
    /*-----------------------------------------------------------*/
    ```


