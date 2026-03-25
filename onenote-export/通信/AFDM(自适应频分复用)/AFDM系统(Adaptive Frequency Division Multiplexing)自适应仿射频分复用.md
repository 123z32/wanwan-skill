# AFDM系统(Adaptive Frequency Division Multiplexing)自适应仿射频分复用

> 来源: OneNote > 通信 > AFDM(自适应频分复用)
> 修改: 2025-12-12T10:00:07Z

AFDM系统(Adaptive Frequency Division Multiplexing)自适应仿射频分复用
 
 
 
 
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-68a3799202114ecfbe5037688e443b82!1-9E53C6D99C1E5AD1!s8f5720a18dc64d48bc8196acc01345ef/$value)
 
AFDM的结构图

 
相较于OFDM系统，原IFFT/FFT部分被IDAFT与DAFT所替代，而利用参数矩阵分解的性质可以得到上述所示的调制解调结构，即只需在IFFT/FFT前后加上相应的Chirp乘积即可。且AFDM也有与CP对应的CPP过程，可以兼容现有的OFDM体制。

 

 
AFDM和OFDM的时频结构如图2-16所示。(a)是OFDM时频结构图，(b)是AFDM时频结构图（与OCDM类似）。OFDM每一个子载波都是频率单一的正弦波，由于OFDM依靠FFT进行数字实现，故可以看到在频域上存在子载波的周期延拓。AFDM的子载波则是由Chirp组成，每一个子载波在时频域上并不交叠，保持正交性，并可以看到在时频域上AFDM各个子载波频率随时间线性变化。利用DAFT进行数字实现，同样可以观察到AFDM各个子载波在频域上的周期延拓现象。在对应带宽下截取一部分频率以进行传输，可以看到AFDM子载波存在的循环移位的现象。

 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-bb054fb68d8147cab56608d6537259fb!1-9E53C6D99C1E5AD1!s8f5720a18dc64d48bc8196acc01345ef/$value)