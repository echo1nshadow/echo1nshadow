#### stm32cubemx
1. 

#### FreeRTOS移植
1. 

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