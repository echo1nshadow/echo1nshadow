### modbus
1. modbus使用主从关系实现**请求-响应**
2. 通信总是成对发生: 一个​设备​必须​发起​请求，​然后​等待​响应,发起​设备​（主​设备）​负责​发起​每次​交互

#### 协议数据单元(PDU)
1. Modbus PDU​格式​被​定义​为​一个​功能​代码，​后面​跟着​一​组​关联​的​数据
2. 该​数据​的​大小​和​内容​由​功能​代码​定义，​整个​PDU（功能​代码​和​数据）​的​大小​不能​超过 **​253** ​个​字​节
3. ​Modbus​可​访问​的​数据​存储​在​四​个​数据​库​或​地址​范围​的​其中​一个：**线圈​状态**、​**离散​量​输入**、​**保持​寄存器**​和 **​输入​寄存器** 
    内存区块 | 数据类型 | 主设备访问 | 从设备访问
     -- | -- | -- | --
     **线圈状态** | 布尔 | 读/写 | 读/写
     **离散输入** | 布尔 | 只读 | 读/写
     **保持寄存器** | 无符号双字节整型 | 读/写 | 读/写
     **输入寄存器** | 无符号双字节整型 | 只读 | 读/写


#### modbus中的浮点数
1. modbus 读写单位为16bit, 一般的浮点型需要拆成2个单位进行读写
   ```
       static void MB_float2quint16(float input, quint16* arr)
    {
        float * ptr_float = &input;
        #if 0
        unsigned char * ptr_char = reinterpret_cast<unsigned char*>(ptr_float);
        qDebug("0:%x\n", *(ptr_char));
        qDebug("1:%x\n", *(ptr_char+1));
        qDebug("2:%x\n", *(ptr_char+2));
        qDebug("3:%x\n", *(ptr_char+3));
        #endif
        quint16* ptr_quint16 = reinterpret_cast<quint16*>(ptr_float);
        arr[0] = *ptr_quint16;
        ptr_quint16 += 1;
        arr[1] = *ptr_quint16;
    }
    ```
2. 读取回到数组里的数据可以用指针处理
    ```
    m_read_value = *( (float*) &( m_read_arr[0] ));
    ```
    使用指针直接转为 float 型
3. C++ 下指针转换使用 **reinterpret_cast\<type\>(pointer)**, 不能使用C的强制转换
    ```
    unsigned char * ptr_char = reinterpret_cast<unsigned char*>(ptr_float);
    quint16* ptr_quint16 = reinterpret_cast<quint16*>(ptr_float);
    ```