# 运算放大器（简称运放），它的英文全称是Operation Amplifier,简写为OP AMP。顾名思义，运算放大器的初衷是用于执行数学计算，比如加、减、乘、除、函数运算等。在当前的技术条件下，运算放大器的数学运算功能已不再突出，现在主要应用于信号放大及有源滤波器设计。

> 来源: OneNote > EDA 设计与开发知识点 > 新分区 1
> 修改: 2024-04-04T15:20:48Z

运算放大器（简称运放），它的英文全称是Operation Amplifier,简写为OP AMP。顾名思义，运算放大器的初衷是用于执行数学计算，比如加、减、乘、除、函数运算等。在当前的技术条件下，运算放大器的数学运算功能已不再突出，现在主要应用于信号放大及有源滤波器设计。

 
在多数的常规设计中，我们使用运放的理想模型，忽略其内部结构。把它当作一个“具有放大作用的元件”，接上电源，便可以让它发挥放大的作用。所谓理想的运放，它的输入阻抗无穷大，输出阻抗为零，如图2.1。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-e3813747c83d4f2e846b8385319ec3e2!1-9E53C6D99C1E5AD1!216/$value)
 
图2.1 运算放大器模型

 
理想的运放电路分析有两大重要原则贯穿始终，即“虚短”与“虚断”。“虚短”的意思是正端和负端接近短路，即V+=V-,看起来像“短路”;“虚断”的意思是流入正端及负端的电流接近于零，即I+=I-=0,看起来像断路（因为输入阻抗无穷大）。

 
2.1运放的典型应用

 
2.1.1 放大电路

 
- 反相比例放大电路
 
- ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-2b27020d275e43fd8c13a7d2be88382f!1-9E53C6D99C1E5AD1!216/$value)
 
 
图2.2 比例放大电路

 
图2.2是典型的比例放大电路，根据“虚短”及“虚断”法则可以很简单的计算得到结果：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-18c3c7daa1b445a3a57a63f6d5515936!1-9E53C6D99C1E5AD1!216/$value)
 
等式2.1中负号，代表输出和输入相位相差180°。

 
推导过程：

 
（1）、电流的流入等于流出，所以i1=i2+13。由“虚断”法则得知i3=0A，所以i1=i2。

 
因此，根据第一章介绍的“叠加法则”，得到：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-1afdab452984466988737238f0e5c80a!1-9E53C6D99C1E5AD1!216/$value)
 
（2）、又根据“虚短”法则，得知运放的正负两个端等同于“短路”，所以V+=V-。而因为运放的正端子V+被R3下拉至地平面，所以V-=V+=0V，代入等式2.2可得到：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-8e1a543bae8d422cba520f3bf17a3899!1-9E53C6D99C1E5AD1!216/$value)
 
再由等式2.3，进一步得到公式2.1，

 
因为Vout与Vin成线性的比例关系，因此这个典型放大电路被称为比例放大电路。

 
关于R1,R2及R3的选值：

 
1）、R1,R2及R3应该在K级，不宜达到M级；

 
2）、R3应该等于或近似于R1与R2的并联，以消除偏置电流的影响。

 
- 差分放大电路
 
- ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-d22f67dfc88948b1bc888803e6bdb045!1-9E53C6D99C1E5AD1!216/$value)
 
 
图2.3 差分放大电路

 
图2.3为差分放大电路，它是图2.2反相比例放大电路的“变种”。类似与反相比例放大电路的分析方法，可以得到结论：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-6c3274efc462455086f31f546304fad3!1-9E53C6D99C1E5AD1!216/$value)
 
当R1=R3并且R2=R4时，得到等式2.5。这就是此电路命名的由来，它可以对差分信号进行放大。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-934f1d795e6745d79da8cf599b23089a!1-9E53C6D99C1E5AD1!216/$value)
 
- 同相放大电路
 

 
上文介绍的放大电路会引起相位翻转180°，图2.4为同相放大电路，顾名思义，输出和输入保持相同的相位。理想的运放具有输入阻抗无穷大，输出阻抗无穷小的特点，同相放大电路保持了运放的这种特性。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-d03a71d6ec3348c19654709965bd4f9c!1-9E53C6D99C1E5AD1!216/$value)
 
图2.4 同相放大电路

 
分析图2.4，应用运放的“虚短”，可知V2=V1；此外，因为运放的“虚断”，输出电压的电流全部流经R2和R1，因此V2由R1和R2对Vout分压得到。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-cc6d07caf00842cab271829aae80c6c0!1-9E53C6D99C1E5AD1!216/$value)
 
因此，

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-fa53e8d5ad3348209f50367e3375a87f!1-9E53C6D99C1E5AD1!216/$value)
 
调节R2可以电路的放大倍数。

 
注意，同相放大电路的应用场合具有局限性，一般只用于直流电平的放大，不适合用于交流信号的放大，因为它会将交流信号的直流偏置电压一并放大，从而使其偏置电位发生偏移。带参考电平的反相比例放大电路在信号放大时比较有实用性。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-90dadef95d694cbda616bd44abbc32e4!1-9E53C6D99C1E5AD1!216/$value)
 
实际上只是在图2.3的差分放大器的基础上加一个隔直电容C1,具体原理待日后讲解有源滤波器时再分析。

 
- 电压跟随电路
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-8bf512a449074a678cd1bdbd3d549798!1-9E53C6D99C1E5AD1!216/$value)
 
图2.5 电压跟随电路

 
图2.5是运放的一种特殊应用方式，很容易得到结论Vout=Vin。输出电压跟随输入电压，因此称之为“电压跟随器”。

 
电压跟随电路是图2.4同相放大电路的衍生产物，是放大倍数为1的同相放大电路。前文已介绍理想的同相放大电路的输入阻抗无穷大，输出阻抗无穷小。

 
基于此特性，电压跟随电路一般用于信号的隔离。简单举例说明，如图2.6，由R1和R2产生参考电压供给下一级电路使用，因为下一级电路的等效内阻会影响R1和R2的分压比，因此参考电压将会发生变化，如果内阻不是固定的，则此电路将无法使用。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-6093790095a04fe9bf56d37e7d4ba314!1-9E53C6D99C1E5AD1!216/$value)
 
图2.6 不可靠的参考电压电路

 
比较可靠的设计如图2.7所示：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-8c7fbc9b5e9f482ba8656912c51bdf9a!1-9E53C6D99C1E5AD1!216/$value)
 
图2.7 可靠的参考电压电路

 
仪器放大电路

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-bf2b5a94b64a4410845aa1552b6f577b!1-9E53C6D99C1E5AD1!216/$value)
 
图2.8 仪器放大电路

 
图2.8是典型的仪器放大电路，顾名思义此方法电路使用于小信号的放大，一般用于传感器信号的放大。传感器的输出信号很小，一般只有几毫伏到几十毫伏。

 
电路由两级放大电路组成，第一级由A1,A2组成，同相输入，输入阻抗高，电路结构对称，可很好的抑制零点漂移；第二级由A3组成，良好的共模抑制比，输入阻抗高，增益在大范围内可调。

 
选值要求：R4=R5,R6=R7,R8=R9（保持电路的对称性），R3为可调电阻，用于调节电路增益。电路输入输出的关系式如下：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-2d5874bd58144b9a94c4469f4ad3764e!1-9E53C6D99C1E5AD1!216/$value)
 
推导过程：

 
实际上，仪器放大电路是前文所述的同相放大电路及差分放大电路的综合体。分析方法可以参考前文的阐述。

 
（1）、首先分析由A1和A2组成的同相放大电路。

 
由“虚短”及“虚断”原则，推导得到：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-f9abaaf2a61f45e4abdbbed8320fb0a2!1-9E53C6D99C1E5AD1!216/$value)
 
（2）、进一步分析由A3组成的差分放大电路。

 
由“虚短”及“虚断”原则，推导得到：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-5f3fc45301644fb087f81931faa19ffd!1-9E53C6D99C1E5AD1!216/$value)
 
（3）、联合等式2.9和2.10得到结论：

 
- 比较器
 
1）、简单的比较器

 
图2.9 简单的比较器

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-7f0b6c0123334b63976da41d77ed3b48!1-9E53C6D99C1E5AD1!216/$value)
 
图2.9是最简单的比较器电路，它利用的原理是“理想的运放具有无穷大的增益”。因此，V+与V-之间稍有电压差，即可引起输出的翻转。微弱的电压差经运放放大引起输出饱和。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-2427d9f02af74d8b961b7df629b70775!1-9E53C6D99C1E5AD1!216/$value)
 
Av为运放的开环放大倍数（一般为100dB左右，即十万倍）。当V+大于V-时，输出为正饱和（接近VCC，但是无法达到）；当V-大于V+时，输出为负饱和（接近-VSS，但是无法达到）。连接V+至地，构成过零比较器，如图2.10所示。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-601c663ccff64543a5f8345bff867458!1-9E53C6D99C1E5AD1!216/$value)
 
图2.10 过零比较器

 
图2.10的过零比较器虽然简单，但是并不实用，它的问题在于比较器只有一个临界电压，输入信号上的杂波易引起输出误操作，如图2.11所示。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-e63b40fc61c94f7d99fcd996ac2840dd!1-9E53C6D99C1E5AD1!216/$value)
 
图2.11，信号杂波引起的比较器误操作

 
2）、迟滞比较器（The hysteresis comparator）

 
相对于上文所述的简单比较器，比较实用的是迟滞比较器，如图2.12所示。

 
图2.12，迟滞比较器

 
相比简单比较器，迟滞比较器只是增加了一个电阻R2。这将引起怎样的微妙变化呢？

 
通俗地说，R2在输入与输出之间搭起了一座桥梁，输出的变化可以通过R2传递至输入，然后比较器的阈值将随输出的变化而改变，达到了磁滞的目的。

 
如果需要定量分析，所有的比较器的原理都是一样的，利用运放的放大倍速为“无穷大”，将V+与V-之间的微弱电压差进行放大，达到饱和输出。所以，首先计算比较器的临界电压值（V+），得到等式2.11。

 
显然，R2的作用是将输出电压引入临界电压。因为Vout会有两种状态+Vsat和-Vsat,所以迟滞比较器也将有两个临界电压（Vth_H及Vth_L）。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-898c26d642c94d2fad9e3d9a297af2b8!1-9E53C6D99C1E5AD1!216/$value)
 
表格2.1，迟滞比较器的状态表

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-5d4fc2354f55409c8cc2117fdef1db6f!1-9E53C6D99C1E5AD1!216/$value)
 
表格2.1可以很好的解释迟滞比较器的工作原理，图2.8是另一种有效的表达迟滞比较器工作原理的方式。设计合适的Vth_H及Vth_L，使(Vth_H-Vth_L)大于杂波幅值，可以有效的避免因为输入信号上的杂波引起的误操作。

 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-3ed35fdbcacd4ffa820d333f8cabc1d9!1-9E53C6D99C1E5AD1!216/$value)
 
图2.13，迟滞比较器的状态矢量图

 

 
3）、窗口比较器

 

 
窗口比较器用于判别输入电压是否落在某一个范围之内，图2.14是典型的窗口比较器。

 
其中，URH>URL，D1和D2不能省略，防止两个运放输出电平相反时损坏运放。比如，运放A1输出VOH，但是运放A2输出VOL,D1导通，但是D2截止，因此电流不会从A1流入A2,避免大电流损坏器件。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-c0bcd1a9e20246ab83b9ac5f222e9445!1-9E53C6D99C1E5AD1!216/$value)
 
图2.14，窗口比较器

 

 
窗口比较的工作原理如图2.15所示。

 
1）、Uin>URH>URL，A1输出UOH,A2输出UOL，D1导通，D2截止，Uout=UOH;

 
2）、Uin<URL<URH，A1输出UOL,A2输出UOH，D1截止，D2导通，Uout=UOH;

 
3）、URL< Uin<URH，A1输出UOL,A2输出UOL，D1截止，D2截止，Uout=UOL;

 
图2.15，窗口比较器的逻辑

 

 来自 <[https://zhuanlan.zhihu.com/p/27595184> 
 

 

 

 

 

 

 

 来自 <[https://zhuanlan.zhihu.com/p/27595184>