##### 微型光谱仪
1. pin 脚
   ![pin](pin.png)
   ![pin2](pin2.png) 
2. 时序
   ![timing](timing.png)
   ![timing2](timing2.png)
   f<sub>CLK</sub> 最大为 5 MHz, 最小为 0.2 MHz
   T<sub>CLK</sub> = 1 / f<sub>CLK</sub>
   tpi(ST) = 381/f
   thp(ST) = 6/f
   tlp(ST) = 375/f
   T<sub>integration</sub> = thp(ST) + 48*f<sub>CLK</sub>
   