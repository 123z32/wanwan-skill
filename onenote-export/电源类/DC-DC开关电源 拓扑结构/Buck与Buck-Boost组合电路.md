# Buck与Buck-Boost组合电路

> 来源: OneNote > 电源类 > DC-DC开关电源 拓扑结构
> 修改: 2025-10-31T17:30:33Z

Buck与Buck-Boost组合电路
 
 
 
 
 

 
金升阳K78系列的产品采用了Buck降压型的电路结构进行设计，是LM78XX系列三端线性稳压器的理想替代品，效率最高可达96%，不需要额外增加散热片，同时还兼有短路保护和过热保护，值得说明的是它能够完美支持负输出。

 

 
　　上面提到金升阳K78系列产品可以支持负输出，这是怎么做到的呢？

 

 
　　从上面Buck电路以及Buck- Boost电路结构原理来看，主要的区别是两者二极管与功率电感的位置互换。因此，若将Buck电路的输出Vo引脚接成输入的GND，而之前的输入GND

 
就变成了负电压输出了，即变成了Buck-Boost的电路结构。对应到金升阳K78xx-500R2系列的产品就变成了如下图6所示的负输出。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-8ef7dda89dd242f0b20928202b81db52!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value)
 

 
　

 
　　因此，用2只K7812-500R2的产品，实现BUCK与BUCK-BOOST电路相结合，可以得到±12V输出，低的纹波和噪声可以给运放进行供电。

 

 
　　

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-9e64ce74d7b34ff8a52aeeb456cf13c6!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value)
 

 
　　需要值得注意的是，由于BUCK-BOOST电路在启动电流会比BUCK电路大一些，所以会在BUCK-BOOST电压输入端加一些缓冲类的器件。