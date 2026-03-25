# LDO(线性电源)

> 来源: OneNote > 电源类 > LDO(低压差线性稳压器）
> 修改: 2025-10-31T15:39:13Z

LDO(线性电源)
 
 
 
 
 

 
一、简介

 
LDO（low dropout regulator，低压差线性稳压器）。这是相对于传统的线性稳压器来说的。传统的线性稳压器，如78XX系列的芯片都要求输入电压要比输出电压至少高出2V~3V，否则就不能正常工作。但是在一些情况下，这样的条件显然是太苛刻了，如5V转3.3V，输入与输出之间的压差只有1.7v，显然这是不满足传统线性稳压器的工作条件的。针对这种情况，芯片制造商们才研发出了LDO类的电压转换芯片

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-ec8c8dcb07414b1684599bd1b73636cd!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 
二、分类

 
PMOS LDO：

 
常见的LDO是由P管构成的，由于LDO效率比较低，因此一般不会走大电流。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-c4ee1a20952041a49c0cc61b8f3df027!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 

 
NMOS LDO：

 
针对某些大电流低压差需求的场合，NMOS LDO应运而生。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-7698d720d92940058e68e6853c2190cf!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 
传统PNP LDO：

 
正输出电压的LDO（低压降）稳压器通常使用功率晶体管（也称为传递设备）作为PNP。这种晶体管允许饱和，所以稳压器可以有一个非常低的压降电压，通常为 200mV 左右。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-3f5a7914f291440bb54fa1787b90611f!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 

 
传统NPN LDO：

 
使用 NPN 复合电源晶体管的传统线性稳压器的压降为2V左右。负输出LDO使用 NPN 作为它的传递设备，其运行模式与正输出 LDO 的 PNP设备类似。

 

 
三、工作原理

 
LDO=low dropout regulator，低压差+线性+稳压器。

 

 
 
- 低压差： 输出压降比较低，例如输入3.3V，输出可以达到3.2V。
 
- 线性： LDO内部的MOS管工作于线性电阻。
 
- 稳压器： 说明了LDO的用途是用来给电源稳压。
 

 
3.1 内部结构

 
以PMOS LDO为例：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-cd518fcdc0ed418580d3840224ba76f2!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 
LDO内部基本都是由4大部件构成，分别是分压取样电路、基准电压、误差放大电路和晶体管调整电路。

 
 
- 分压取样电路： 通过电阻R1和R2对输出电压进行采集；
 
- 基准电压： 通过bandgap（带隙电压基准）产生的，目的是为了温度变化对基准的影响小；
 
- 误差放大电路： 将采集的电压输入到比较器反向输入端，与正向输入端的基准电压（也就是期望输出的电压）进行比较，再将比较结果进行放大；
 
- 晶体管调整电路： 把这个放大后的信号输出到晶体管的控制极（也就是PMOS管的栅极或者PNP型三极管的基极），从而这个放大后的信号（电流）就可以控制晶体管的导通电压了，这就是一个负反馈调节回路。
 

 
3.2 负反馈流程

 
以PMOS LDO为例：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-7777273033424de7ba6ac37e54d5638e!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 

 
反馈回路

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-5c352e0565c64042a802d20ba3535880!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 
PMOS驱动的反馈

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-bb386726558d4a77a4d27bbc055c38eb!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-81cf377e015246b1a8ea598d5a82208e!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 

 
四、主要参数

 
输入输出压差（Dropout Voltage）：

 
对于LDO来说，输入电压是高于输出电压的，但是两者压差一般都是很小，LDO的输入电流几乎等于输出电流，因此压差越大，效率越低（本身吃掉了很多能量电流×晶体管压降），压差越小，LDO电压转换效率越高以及能量损耗越小。

 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-35c1c1f92b4e409786c81a80351be024!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-0a6b42a6463d410188ff319e758b11e4!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 
 
- 电源抑制比（PSRR）：
 

 
LDO的 PSRR数据是用来量化LDO对不同频率的输入电源纹波的抑制能力的，它反映了LDO不受噪声和电压波动、保持输出电压稳定的能力。在特定频段内，PSRR越大越好。

 
100K到1MHz内的PSRR非常重要，这个是DCDC的噪声频率范围，LDO经常作为DCDC的下一级，要有能力滤除来自DCDC的大量噪声。

 
在ADC，DAC，Camera的AVDD供电上，我们要选择PSRR大于80dB（@100Hz）的LDO。LDO的环路控制往往是确定电源抑制性能的主要因素，同时大容量，低ESR的电容对电源一直也非常有用，建议选择陶瓷电容。

 

 
PSRR与频率有关，LDO的规格书一般会给出几个频点的PSRR值。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-8fba4515a7404c64a775a80cebfdbff1!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 

 

 
 
- 噪声（Noise）：
 

 
不同于PSRR，噪声是指LDO自身产生的噪声信号，低噪声的LDO稳压芯片可以很好的降低LDO产生的额外噪声，输出的电压更纯净，噪声一般计算出的值是有效值(rms)，也可以用peak to peak来分析。

 

 
如下是某LDO的噪声水平，通常在uV级别。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-710807d222914aff9cb58179f2ec97ed!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 

 

 
LDO输出噪声的另一种表示方式是噪声频谱密度。只有高精度，低噪声电路上才需要关注这个参数。

 
 
- 静态电流（Iq）：
 
静态电流（Quiescent Current）是外部负载电流为0时，LDO内部电路供电所需的电流。内部电路包括带隙基准电压源、误差放大器、输出分压器以及过流和过温检测电路。这个电流经过从LDO的GND流出。

 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-df371aa5939b4c77aecb72cc65cb7576!1-9E53C6D99C1E5AD1!s54889e5596e04debac8a5a86ae0bfd63/$value)
 
在一些电池供电低功耗场景下，要考虑LDO本身自身消耗的静态电流。休眠阶段的电源消耗成为影响电池寿命的关键因素。要想最大限度地降低睡眠期间的功率消耗，选择具有极低静态电流的器件就是必须的。一般LDO芯片的静态电流的大小与芯片的其他性能成反关系，如低噪声，高电源电压抑制比，动态性能好的LDO静态电流都偏大一些。低IQ的LDO做的好的话＜100nA。