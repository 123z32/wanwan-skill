# ADC(PC8591)

> 来源: OneNote > 单片机 > IAP152K61S2
> 修改: 2025-06-11T14:25:48Z

ADC(PC8591)
 
 
 
 
 

 
PCF8591是一款单芯片、单电源、低功耗8位CMOS数据采集设备

 
具有四个模拟输入、一个模拟输出和一个串行12c总线接口。

 
三个地址引脚AO, A1和A2用于编程硬件地址，允许使用多达8个设备连接到12c总线而不需要额外的硬件。

 
地址、控制和数据通过两路双向12c总线串行地传送到和从设备。

 
该装置的功能包括模拟输入多路复用、片上跟踪和保持功能、8位模数转换和8位数模转换。最大转换速率由12c总线的最大速度给出。

 

 
特性

 
 
- 单电源
 
- 工作电源电压2.5 V ~ 6v
 
- 低待机电流
 
- 通过12c总线串行输入/输出
 
- 地址由3个硬件地址引脚决定
 
- 采样率由12c总线速度决定
 
- 给出4个模拟输入，可编程为单端或差分输入
 
- 可选择自动递增通道
 
- 模拟电压范围从Vss到Vdd
 
- 片上跟踪和保持电路
 
- 8位逐次逼近A/D转换
 
- 一个DAC模拟输出
 

 

 

 
总体

 
框图

 ![在这里插入图片描述](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-7b67f693dd114a4987773720c8d3ea5f!1-9E53C6D99C1E5AD1!s99d9fe3c69c547509269318053602ce7/$value)
 
引脚

 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-e4e117d786274ff59a675cb79b6e2b92!1-9E53C6D99C1E5AD1!s99d9fe3c69c547509269318053602ce7/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-6af03cb49126440bb1da8ce09d2470a7!1-9E53C6D99C1E5AD1!s99d9fe3c69c547509269318053602ce7/$value)
 

 

 
功能描述

 

 
寻址

 
i2c总线系统中的每个PCF8591设备通过发送一个有效的地址来寻址。

 
地址由固定部分和可编程部分组成。

 
可编程部分必须根据地址引脚AO、A1和A2进行设置。

 
地址总是必须作为12c总线协议中的开始条件之后的第一个字节被发送。

 
地址字节的最后一位是读写位，它设定了接下来数据传输的方向(见下图)。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-50a83de45ecd400f944d38aee27e4a3d!1-9E53C6D99C1E5AD1!s99d9fe3c69c547509269318053602ce7/$value)
 

 
注：最后一位为0是写，最后一位为1是读

 

 
控制字节

 
发送到PCF8591设备的第二个字节将存储在其控制寄存器中，并需要控制设备的功能。

 
控制寄存器的高4位用于使能模拟输出，并将模拟输入编程为单端或差分输入。

 
低4位选择由高4位所定义的模拟输入通道之一。

 
如果设置了自动增量标志，在每次A/D转换后，通道号会自动增加。

 
如果在使用内部振荡器的应用中需要自动增量模式，则应该设置控制字节(第6位)中的模拟输出使能标志。

 
这允许内部振荡器连续运行，从而防止由振荡器启动延迟导致的转换错误。

 

 
上电复位后，控制寄存器的所有位都复位为逻辑0。为了省电，D/A转换器和振荡器被禁用。模拟输出被切换到高阻抗状态。

 ![在这里插入图片描述](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-9bc6d47facc642ce978d8d436a0c48a1!1-9E53C6D99C1E5AD1!s99d9fe3c69c547509269318053602ce7/$value)
 
D/A转换

 
发送到PCF8591设备的第三个字节存储在DAC数据请求器中，并使用片上D/ A转换器转换为相应的模拟电压。

 
这个D/A转换器由一个电阻分频链组成，

 
该分频链连接到具有256个分频点和选择开关的外部参考电压。tap-decoder将其中一个tap切换到DAC输出线(见下图)。

 
模拟输出电压由一个自动归零的放大器缓冲。

 
这个缓冲放大器可以通过设置模拟输出使能标志来打开或关闭控制寄存器。

 
在使能状态下，输出电压被保持直到进一步的数据字节被发送。片上D/A转换器也用于逐次逼近A/D转换。为了释放DAC进行A/D转换循环，单位增益放大器配备了跟踪和保持电路。

 
这个电路在执行A/D转换时保持输出电压。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-0ba2612e96d240c087a3e8c0301ca979!1-9E53C6D99C1E5AD1!s99d9fe3c69c547509269318053602ce7/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-51026d51a8434bcfbbddb0f7789babfb!1-9E53C6D99C1E5AD1!s99d9fe3c69c547509269318053602ce7/$value)
 
D/A转换过程

 ![在这里插入图片描述](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-bc5530a69e4d48e2979bbb935ba8a33b!1-9E53C6D99C1E5AD1!s99d9fe3c69c547509269318053602ce7/$value)
 ![在这里插入图片描述](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-1f26787a907a4953a591cc780c10b200!1-9E53C6D99C1E5AD1!s99d9fe3c69c547509269318053602ce7/$value)
 

 

 
注意: S为IIC开始信号,P为IIC停止信号

 
要使用D/A转换，必须使能模拟输出，然后根据流程，首先

 
IIC开始信号->PCF8591地址写->等待PCF8591回应->控制字节->等待PCF8591回应->DAC的值->等待PCF8591回应->DAC的值…

 
这个DAC的值可以一直改变，只要没有重新IIC开始信号，或者结束信号，DAC输出就一直是最后一个输出的值!!

 

 
void PCF8591_DAC(u8 dac_Data)

 
{

 
I2CStart();//IIC开始信号

 
I2CSendByte(0x90);//PCF8591地址写

 
I2CWaitAck();//等待PCF8591回应

 
I2CSendByte(0x40);//控制字节

 
I2CWaitAck();//等待PCF8591回应

 
I2CSendByte(dac_Data);//DAC的值

 
I2CWaitAck();等待PCF8591回应

 
I2CStop();//IIC结束信号

 
}

 

 
A/D转换

 
A/D转换器采用逐次逼近转换技术。

 
在A/D转换周期内临时使用片上D/A转换器和高增益比较器。

 
A/D转换周期总是在发送一个有效的读模式地址到PCF8591设备后开始。

 
A/D转换周期在应答时钟脉冲的后缘触发。

 
一旦转换周期被触发，所选通道的输入电压样本被存储在芯片上转换成相应的8位二进制码。

 
从差分输入中提取的样本被转换成一个8位的转换结果存储在ADC数据寄存器并等待传输。

 
如果设置了自动增量，则选择下一个通道。

 
在一个读周期中传输的第一个字节包含前一个读周期的转换结果代码。

 
在上电复位条件后，第一个字节读取为十六进制80。

 
最大A/D转换速率是由12c总线的实际速度给出的。

 
A/D转换过程

 ![在这里插入图片描述](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-7cbf004bc793404eb7e3516da0af0142!1-9E53C6D99C1E5AD1!s99d9fe3c69c547509269318053602ce7/$value)
 ![在这里插入图片描述](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-9ba779b726014b59830d74afb01327bc!1-9E53C6D99C1E5AD1!s99d9fe3c69c547509269318053602ce7/$value)
 
意思就是说，在开始读后，读的是上一次转换的结果！

 
流程为：IIC开始信号->地址读->等待PCF8591回应

 
->读PCF8591->主机回应->继续读->主机回应…->直到想停止AD转换了->不回应了->直接停止信号

 

 
（需要写入控制字节选择输入通道）

 

 
void PCF8951_init()

 
{

 
I2CStart();

 
I2CSendByte(0x90);

 
I2CWaitAck();

 
I2CSendByte(0x43);//DACOUT ADC IN1;

 
I2CWaitAck();

 
I2CStop();

 
}

 

 
5/256=0.01953

 
V*0.01953

 
MV*19.53

 

 
void PCF8951_ADC()

 
{

 
I2CStart();

 
I2CSendByte(0x91);

 
I2CWaitAck();

 
ADC_value=I2CReceiveByte()*19.53;//mV ****

 
I2CWaitAck();

 
I2CStop();

 
}

 

 
假如需要读跟写则初始化，写入控制字节。