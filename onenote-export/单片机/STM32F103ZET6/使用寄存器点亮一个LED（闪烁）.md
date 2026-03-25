# 使用寄存器点亮一个LED（闪烁）

> 来源: OneNote > 单片机 > STM32F103ZET6
> 修改: 2025-02-03T06:49:44Z

使用寄存器点亮一个LED（闪烁）
 
 
 
 
 

 
硬件设计 

 
开发板上LED电路图如图7.2.1所示。 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-77729976327241c3af2e28ee66a238ff!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
相同网络标号表示它们是连接在一起的，因此D1-D8发光二极管阴极是连接 在STM32 的PC0-PC7管脚上。如果要使D1指示灯亮，只需要控制PC0管脚输出 低电平，如果要使D1指示灯灭，只需控制PC0输出高电平。对于其他的LED控制方法一样。如果你们使用的是其他板子，连接LED的管脚和极性不一样，那么 只需要在程序中修改对应的GPIO管脚和输出电平状态即可，原理是一样的。 本章我们所要实现的功能是点亮D1发光二极管，即让STM32的PC0管脚输出一个低电平。

 

 
软件设计

 
 在“寄存器模板创建”章节中已经创建了一个寄存器工程模板，这里面我们 直接复制这个模板到本章的实验中，在此模板基础上进行程序编写。前面寄存器 模板创建的时候我们使用到了3个文件，一个是startup_stm32f10x_hd.s启动文件，一个是main.c文件，还有一个是stm32f10x.h文件。main.c和stm32f10x.h 文件内没有内容，只有startup_stm32f10x_hd.s文件有，我们就来了解下这个启动文件内部的一些东西。

 
 启动文件里边是使用汇编语言写好了基本程序，当STM32 芯片上电启动的 时候，首先会执行这里的汇编程序，从而建立起 C 语言的运行环境，所以我们把这个文件称为启动文件。该文件使用的汇编指令是 Cortex-M3内核支持的指令，可参考《 Cortex-M3 权威指南中文》内指令集章节。

 
 startup_stm32f10x_hd.s 文件是由 ST 官方提供的，一般有需要也是在官方 的基础上修改，不会自己完全重写。该文件可以从 KEIL5 安装目录找到，也可 以从 ST 库里面找到，找到该文件后把启动文件添加到工程里面即可。不同型号 的芯片以及不同编译环境下使用的汇编文件是不一样的，但功能相同。

 

 
对于启动文件这部分我们主要总结它的功能，不详细讲解里面的代码，其功能如下：

 
 初始化堆栈指针 SP; 

 
 初始化程序计数器指针 PC; 

 
 设置堆、栈的大小; 

 
 设置中断向量表的入口地址; 

 
 配置外部SRAM 作为数据存储器（这个由用户配置，一般的开发板可没有外部SRAM）; 

 
 调用SystemInit() 函数配置 STM32 的系统时钟。 

 
 设置C 库的分支入口“ __main”（最终用来调用 main 函数） ;

 

 
先去除繁枝细节，挑重点的讲，主要理解最后两点，在启动文件中有一段复位后立即执行的程序，

 

 
在实际工程中阅读时，可使用编辑器的搜索(Ctrl+F)功能查找这段代码在文件中的位置。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-e889c26fa14c468c94c4c405206b4d29!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
开头148行的是程序注释，在汇编里面注释用的是“ ;”，相当于 C 语言 的“ //”注释符 

 

 
第149行是定义了一个子程序： Reset_Handler。 PROC 是子程序定义伪指 令。这里就相当于 C 语言里定义了一个函数，函数名为 Reset_Handler。 

 

 
第150行 EXPORT 表示 Reset_Handler 这个子程序可供其他模块调用。 相 当于 C 语言的函数声明。关键字[WEAK] 表示弱定义，如果编译器发现在别处定 义了同名的函数，则在链接时用别处的地址进行链接，如果其它地方没有定义， 引入函数声明。以便下面对外部函数进行调用。 编译器也不报错，以此处地址进行链接，如果不理解 WEAK，那就忽略它好了。

 

 
 第151行和第152行 IMPORT 说明 __main 和SystemInit 这两个标号在其 他文件，在链接的时候需要到其他文件去寻找。相当于 C 语言中，从其它文件 SystemInit 需要由我们自己实现，即我们要编写一个具有该名称的函数， 用来初始化STM32 芯片的时钟，一般包括初始化 AHB、 APB 等各总线的时钟， 需要经过一系列的配置 STM32 才能达到稳定运行的状态。__main 其实不是我们 定义的(不要与 C 语言中的 main 函数混淆)，当编译器编译时，只要遇到这个 标号就会定义这个函数，该函数的主要功能是：负责初始化栈、堆，配置系统环 境，准备好 C 语言并在最后跳转到用户自定义的 main 函数，从此来到 C 的世 界。

 

 
第153行把 SystemInit 的地址加载到寄存器 R0。

 

 
第154行程序跳转到 R0 中的地址执行程序，即执行 SystemInit 函数的内 容。 

 

 
第155行把__main 的地址加载到寄存器 R0。

 
第156行程序跳转到 R0 中的地址执行程序，即执行__main 函数，执行完 毕之后即可进入 main 函数。 第157行表示子程序的结束。 总之，看完这段代码后，了解到如下内容即可：我们需要在外部定义一个 SystemInit 函数设置 STM32 的时钟； STM32 上电后，会执行 SystemInit 函 数，最后执行我们 C 语言中的 main 函数。 下面就开始使用寄存器来操作STM32使PC0输出一个低电平。要操作STM32 寄存器，我们就需要使用C语言对其封装，这部分程序我们都放在stm32f10x.h 中。具体代码如下：

 

 
#define PERIPH_BASE ((unsigned int)0x40000000)

 
 #define APB2PERIPH_BASE (PERIPH_BASE + 0x00010000)

 
 #define GPIOC_BASE (APB2PERIPH_BASE + 0x1000)

 
 #define GPIOC_CRL *(unsigned int*)(GPIOC_BASE+0x00)

 
 #define GPIOC_CRH *(unsigned int*)(GPIOC_BASE+0x04)

 
 #define GPIOC_IDR *(unsigned int*)(GPIOC_BASE+0x08)

 
 #define GPIOC_ODR *(unsigned int*)(GPIOC_BASE+0x0C)

 
 #define GPIOC_BSRR *(unsigned int*)(GPIOC_BASE+0x10)

 
 #define GPIOC_BRR *(unsigned int*)(GPIOC_BASE+0x14)

 
 #define GPIOC_LCKR *(unsigned int*)(GPIOC_BASE+0x18)

 
 #define AHBPERIPH_BASE (PERIPH_BASE + 0x20000)

 
 #define RCC_BASE (AHBPERIPH_BASE + 0x1000)

 
 #define RCC_APB2ENR *(unsigned int*)(RCC_BASE+0x18)

 

 
要控制PF9输出低电平，需知道GPIO这个外设它是挂接在哪个总线上的， 通过Block2外设基地址及APB2总线的偏移地址就可以得到APB2外设的基地址。 GPIO 就是挂接在APB2总线上的，根据GPIOC的偏移地址就可以得到GPIOC外设的基地址，GPIOC外设内部含有很多个寄存器，比如GPIOC_CRL、GPIOC_CRH端口配置寄存器、GPIOC_BSRR置位复位寄存器等，通过他们各自的偏移地址就可以获取对应的寄存器地址，然后要操作地址里面的内容就需要使用到指针，将其强制转换为unsigned int*指针类型，然后在通过一个*指针来操作该地址里面要控制PF9输出低电平，需知道GPIO这个外设它是挂接在哪个总线上的，通过Block2外设基地址及APB2总线的偏移地址就可以得到APB2外设的基地址。 GPIO 就是挂接在APB2总线上的，根据GPIOC的偏移地址就可以得到GPIOC外设 的基地址，GPIOC外设内部含有很多个寄存器，比如GPIOC_CRL、GPIOC_CRH端口配置寄存器、GPIOC_BSRR置位复位寄存器等，通过他们各自的偏移地址就可 以获取对应的寄存器地址，然后要操作地址里面的内容就需要使用到指针，将其 强制转换为unsigned int*指针类型，然后在通过一个*指针来操作该地址里面的内容。在STM32中凡是使用到外设功能，都要使能对应的外设时钟，否则即使 配置好端口初始化也无法正常使用。因此还需要知道时钟RCC外设的基地址，通 过《STM32F103ZET6 数据手册》“4 Memory mapping”的“存储器映射”章节可 以知道RCC时钟外设是挂接在AHB总线上，根据其偏移值可以得到RCC时钟外设 的基地址，然后可通过《STM32F1xx中文参考手册》的“6 小容量、中容量和大 容量产品的复位和时钟控制(RCC)”的“6.3.7 APB2 外设时钟使能寄存器 (RCC_APB2ENR)”可找到对应的端口RCC使能寄存器，只要将GPIOC端口时钟使能即可

 
点亮一个LED

 
#include "stm32f10x.h" // Device header

 

 
void SystemInit()

 
{

 

 
}

 

 
int main()

 
{

 
RCC_APB2ENR|=1<<4;//开启GPIOC时钟

 
GPIOC_CRL &=~(0X0F<<(4*0));//配置GPIOC为通用推完输出模式

 
GPIOC_CRL|=(3<<4*0);

 
GPIOC_BSRR=(1<<(16+0));//使 PC0 输出低电平。

 

 
while(1)

 
{

 

 
}

 
}

 
（1）包含stm32f10x.h头文件，在这个头文件中我们定义的都是寄存器， 因此如果要在其他文件中使用这些寄存器就需要把这个头文件包含进来，否则编译就会报错。 

 
（2）SystemInit 函数，在前面讲解启动文件时已经说明，程序运行的时候先进入这个函数进行STM32的初始化，如果不写这个函数编译器就会报错。这里 我们编写这个函数，里面并不对其操作。 

 
（3）开启GPIOC时钟。要使PC0正常工作输出一个低电平，必须要打开它 的时钟。RCC_APB2ENR 寄存器是在stm32f10x.h 头文件中定义好的，只要查下 《STM32F1xx 中文参考手册》RCC时钟使能寄存器内容就可以知道此寄存器的第 4 位是控制GPIOC外设的时钟使能位，只有该位为1时才使能，如果为0即关闭 GPIOC 时钟。所以要让1左移4位。 

 
（4）配置GPIOC为通用推完输出模式。STM32的GPIO模式有很多，可根据 CRx 寄存器设置，CRL对应GPIO的低8位，CRH对应GPIO的高8位。如果不是 特殊需求，一般输出采用推完输出模式。我们要让PC0管脚输出一个低电平，故 使用推完输出模式。只要查下《STM32F1xx中文参考手册》GPIO配置寄存器内容 就可以知道此寄存器内每4位控制一个管脚。 

 
（5）使 PC0 输出低电平。GPIOC_BSRR 为置位复位寄存器，只要查下 《STM32F1xx中文参考手册》GPIO置位复位寄存器内容就可以知道，其高16位用于复位，如果当高16位某位为1，表示那一位管脚输出低电平，为0不影响 其输出电平。如果当低16位的某位为1，表示那一位管脚输出高电平，为0不 影响其输出电平。所以要让1左移16+0位。

 
LED闪烁

 
#include "stm32f10x.h" // Device header

 
typedef unsigned int u16;

 
void SystemInit()

 
{

 

 
}

 

 
void delay_us(u16 t)

 
{

 
while(t--);

 
}

 

 
int main()

 
{

 
RCC_APB2ENR|=1<<4;//开启GPIOC时钟

 
GPIOC_CRL &=~(0X0F<<(4*0));//配置GPIOC为通用推完输出模式

 
GPIOC_CRL|=(3<<4*0);

 
GPIOC_BSRR=(1<<(16+0));//使 PC0 输出低电平。

 

 
while(1)

 
{

 
GPIOC_BSRR=(1<<(16+0));//使 PC0 输出低电平。

 
delay_us(100000);

 
GPIOC_BSRR=(1<<(0));//使 PC0 输出高电平。

 
delay_us(100000);

 
}

 

 
}

 
到这里整个程序就编写完成，我们编译一下，如图7.3.2所示：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-3edb77caa2454b1b85540d880bdb9dac!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
可以看到没有错误，也没有警告。从编译信息可以看出，我们的代码占用 FLASH 大小为：540字节（220+320），所用的 SRAM 大小为：1024个字节（1024+0）。 这里我们解释一下，编译结果里面的几个数据的意义： Code：表示程序所占用 FLASH 的大小。 RO-data：即 Read Only-data，表示程序定义的常量，存储在FLASH内。 RW-data：即 Read Write-data，表示已被初始化的变量，存储在SRAM内。 ZI-data：即 Zero Init-data，表示未被初始化的变量，存储在SRAM内。 有了这个就可以知道你当前使用的flash和sram大小了，所以，一定要注意的 7.4 实验现象 是程序的大小不是.hex 文件的大小，而是编译后的 Code 和 RO-data 之和。