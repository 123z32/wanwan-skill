# 第二章-BJT三极管

> 来源: OneNote > 模电技术基础 > 进入
> 修改: 2025-10-31T07:40:38Z

第二章-BJT三极管
 
 
 
 
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-ade00ab28bfa490b91363cbda33c9965!1-9E53C6D99C1E5AD1!205/$value)
 

 
第二章——BJT三极管.

 

 
[一.BJT的工作原理

 
[二.放大电路的分析方法

 
[三.基本共射极放大电路、共集电极放大电路和共基极放大电路

 

 

 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-663aadf67cfd456eadca177e0a5198b6!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
 

 
一.BJT的工作原理

 
三极管的放大作用是在一定的外部条件控制下，通过载流子传输体现出来的。

 
外部条件：发射结正偏、 集电结反偏。

 
 

 
1.内部载流子的传输过程

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-2fb75f9e16004dd6815f5612d1181bbc!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
 

 
2.电流分配关系

 
（1）电流放大系数 α

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-0d172dba7ae746e4ae23154033d6c256!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
α 为电流放大系数。它只与管子的结构尺寸和掺杂浓度有关，与外加电压无关。一般 α = 0.9~0.99 。

 
 

 
（2）电流放大系数 β

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-3d6394358c264dd6835440f22fcdb50c!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
β 是另一个电流放大系数。同样，它也只与管子的结构尺寸和掺杂浓度有关，与外加电压无关。一般 β >> 1 。

 
 

 
3.三极管的三种组态

 
(a) 共基极接法，基极作为公共电极，用CB表示；

 
(b) 共发射极接法，发射极作为公共电极，用CE表示；

 
© 共集电极接法，集电极作为公共电极，用CC表示。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-08e36ee82f2946d49960c3ad6c0f6f3b!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
综上所述，三极管的放大作用，主要是依靠它的发射极电流能够通过基区传输，然后到达集电极而实现的。

 
实现这一传输过程的两个条件是：

 
（1）内部条件：发射区杂质浓度远大于基区杂质浓度，且基区很薄。

 
（2）外部条件：发射结正向偏置，集电结反向偏置。

 
 

 
 4.BJT的V-I 特性曲线

 
（1）输入特性曲线

 
当vCE=0V时，相当于发射结的正向伏安特性曲线。当vCE≥1V时， vCB= vCE - vBE>0，集电结已进入反偏状态，开始收集电子，基区复合减少，同样的vBE下 IB减小，特性曲线右移。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-fe09bf9a73d74bf6aa8c0e1bac75c864!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
（2）输出特性曲线

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-16e3ae738aa644f892efb51bfb3c66be!1-9E53C6D99C1E5AD1!205/$value)
 

 
 

 
输出特性曲线的三个区域:

 
**饱和区：**iC明显受vCE控制的区域，该区域内，一般vCE＜0.7V (硅管)。此时，发射结正偏，集电结正偏或反偏电压很小。

 
截止区：iC接近零的区域，相当iB=0的曲线的下方。此时， vBE小于死区电压。

 
放大区：iC平行于vCE轴的区域，曲线基本平行等距。此时，发射结正偏，集电结反偏。

 
 

 
5.BJT的主要参数

 
（1）电流放大系数：上边介绍过当Icbo和Iceo很小时，二者可忽略不计。

 
（2）极间反向电流：发射极开路时，集电结的反向饱和电流Icbo、集电极发射极间的反向饱和电流Iceo。

 
（3）极限参数：集电极最大允许电流Icm、集电极最大允许功率损耗Pcm、V(BR)CBO——发射极开路时的集电结反向击穿电压、V(BR) EBO——集电极开路时发射结的反向击穿电压、V(BR)CEO——基极开路时集电极和发射极间的击穿电压。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-5376f3b2878d47668d74d311e4bbf263!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
当温度上升时，BJT的反向电流ICBO、ICEO及电流放大系数都会增大，而发射结正向压降VBE会减小。这些参数随温度的变化，都会使放大电路中的集电极静态电流ICQ随温度升高而增加（ICQ= β IBQ+ ICEO） ，从而使Q点随温度变化。 要想使ICQ基本稳定不变，就要求在温度升高时，电路能自动地适当减小基极电流IBQ 。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-432ec6c10c22403fbb2f09769d98a98f!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
 

 
二.放大电路的分析方法

 
1.图解分析法

 
求解步骤：

 
静态工作点的图解分析（采用该方法分析静态工作点，必须已知三极管的输入输出特性曲线。）：

 
（1）首先，画出直流通路；

 
（2）列输入回路方程；列输出回路方程（直流负载线）；

 
（3）在输入特性曲线上，作出直线vbe = Vbb - ibRb ，两线的交点即是Q点，得到IBQ；

 
（4）在输入特性曲线上，作出直线 Vce = Vcc - icRc ，两线的交点即是Q点，得到IBQ。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-d6d929eb2d06461d9dbaeb26b6cde811!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
**动态工作情况的图解分析：**根据vs的波形，在BJT的输入特性曲线图上画出vBE 、 iB 的波形，根据iB的变化范围在输出特性曲线图上画出iC和vCE 的波形。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-b13106c2face4a5db3621f343aeea12c!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
若静态工作点选择不当，可能会导致截止失真或饱和失真。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-e627c8cdcb8f4f459f98b8e3123eb37f!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
图解分析法的适用范围：幅度较大而工作频率不太高的情况。

 
**优点：**直观、形象。有助于建立和理解交、直流共存，静态和动态等重要概念；有助于理解正确选择电路参数、合理设置静态工作点的重要性。能全面地分析放大电路的静态、动态工作情况。

 
**缺点：**不能分析工作频率较高时的电路工作状态，也不能用来分析放大电路的输入电阻、输出电阻等动态性能指标。

 
 

 
2.小信号模型分析法

 
建立小信号模型的思路：当放大电路的输入信号电压很小时，就可以把三极管小范围内的特性曲线近似地用直线来代替，从而可以把三极管这个非线性器件所组成的电路当作线性电路来处理。详细见“【知识点总结】电路原理 第二讲”

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-0ee38b6d69b64f809dba8f1deb3158cc!1-9E53C6D99C1E5AD1!205/$value)
 
 

 

 
受控电流源hfeib ，反映了BJT的基极电流对集电极电流的控制作用。电流源的流向由ib的流向决定。hre vce是一个受控电压源。反映了BJT输出回路电压对输入回路的影响。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-0fbbd05e5f1346b5b31bc5aa913f5c9c!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
注：H参数都是小信号参数，即微变参数或交流参数；H参数与工作点有关，在放大区基本不变；H参数都是微变参数，所以只适合对交流信号的分析。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-3f40f78fad8542758f40d7950336593e!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
求解步骤：

 
用H参数小信号模型分析基本共射极放大电路：

 
（1）利用直流通路求Q点；

 
（2）画小信号等效电路；

 
（3）求放大电路动态指标，如电压增益、输入电阻、输出电阻。

 
小信号模型分析法的优缺点：

 
**优点：**分析放大电路的动态性能指标(Av 、Ri和Ro等)非常方便，且适用于频率较高时的分析。

 
**缺点：**在BJT与放大电路的小信号等效电路中，电压、电流等电量及BJT的H参数均是针对变化量(交流量)而言的，不能用来分析计算静态工作点。

 
 

 
三.基本共射极放大电路、共集电极放大电路和共基极放大电路

 
1.基本共射极放大电路

 
（1）静态(直流工作状态)

 
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-d9077f454e88480c9a146480d32a281c!1-9E53C6D99C1E5AD1!205/$value)
 
（2）**动态：**输入正弦信号vs后，电路将处在动态工作情况。此时，BJT各极电流及电压都将在静态值的基础上随输入信号作相应的变化。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-dd744bc3e8b44859b1556424dc8a0c7d!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
 

 
2.共集电极放大电路（射极输出器）

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-f49a369519ed412d8fc7c0347a925f31!1-9E53C6D99C1E5AD1!205/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-f5acab6ae94e490e8532a2cac3121b99!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
 

 
注：（以上不列举具体公式）

 
共集电极电路特点：

 
（1）电压增益小于1但接近于1，vo 与 vi同相。

 
（2）输入电阻大，对电压信号源衰减小。

 
（3）输出电阻小，带负载能力强。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-21a62c729fa1483ba345f718af7eb331!1-9E53C6D99C1E5AD1!205/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-30b67101feca4c21a88faffa105bccd9!1-9E53C6D99C1E5AD1!205/$value)
 
计算输出电阻，断开负载RL，并且短接输入ES

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-c23328d895e444bb8295ca2ab5995f7a!1-9E53C6D99C1E5AD1!205/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-dc6c93bb265c4c8ba5022b35d957b4e1!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
 

 
3.共基极放大电路

 
直流通路与射极偏置电路相同。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-89f640002ee34ccdb5f7de81bce76a32!1-9E53C6D99C1E5AD1!205/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-133934abe8364b4e87eb40cd01bc6dc3!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
4.三种组态的判别

 
以输入、输出信号的位置为判断依据：

 
信号由基极输入，集电极输出——共射极放大电路

 
信号由基极输入，发射极输出——共集电极放大电路

 
信号由发射极输入，集电极输出——共基极电路

 
四.射极偏置电路

 
基极分压式射极偏置电路

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-c0092d7e8c38413eaddf2eeafb76e342!1-9E53C6D99C1E5AD1!205/$value)
 
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-0a62e39484ca40a393759031c791483b!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
注：（以上不列举具体公式）

 
除此之外，还有含有双电源的射极偏置电路、含有恒流源的射极偏置电路

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-444291ab8f514ea3ba9fb5009484c8fe!1-9E53C6D99C1E5AD1!205/$value)
 

 
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-302e9bab53b14939a3c8b128f16b1a0a!1-9E53C6D99C1E5AD1!205/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-d533fbe25e8949f7be45745bdc972405!1-9E53C6D99C1E5AD1!205/$value)
 
三种组态的特点及用途：

 
共射极放大电路： 

 
电压和电流增益都大于1，输入电阻在三种组态中居中，输出电阻与集电极电阻有很大关系。适用于低频情况下，作多级放大电路的中间级。

 
共集电极放大电路：

 
只有电流放大作用，没有电压放大，有电压跟随作用。在三种组态中，输入电阻最高，输出电阻最小，频率特性好。可用于输入级、输出级或缓冲级。

 
共基极放大电路：

 
只有电压放大作用，没有电流放大，有电流跟随作用，输入电阻小，输出电阻与集电极电阻有关。高频特性较好，常用于高频或宽频带低输入阻抗的场合，模拟集成电路中亦兼有电位移动的功能。