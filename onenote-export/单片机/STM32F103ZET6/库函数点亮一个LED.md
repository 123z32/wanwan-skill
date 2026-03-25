# 库函数点亮一个LED

> 来源: OneNote > 单片机 > STM32F103ZET6
> 修改: 2025-02-10T12:48:32Z

库函数点亮一个LED
 
 
 
 
 

 
硬件设计

 
在我们开发板上有8个LED连接STM32F103芯片管脚，具体电路如图10.1.1 所示。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-d2e33555f0b94a9aacabb4e83f73d103!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
相同网络标号表示它们是连接在一起的，因此D1发光二极管阴极是连接在 STM32 的 PC0 管脚上，D2指示灯阴极连接在PC1管脚上,其他LED管脚以此类推。 如果要使D1指示灯亮，只需要控制PC0管脚输出低电平，如果要使D1指示灯灭，只需控制PC0输出高电平。如果你们使用的是其他板子，连接LED的管脚和极性 不一样，那么只需要在程序中修改对应的GPIO管脚和输出电平状态即可，原理 是一样的。 本章我们所要实现的功能是点亮D1发光二极管，即让STM32的PC0管脚输出一个低电平。

 

 
软件设计 

 
因为我们采用的是库函数开发，所以需要复制上一章创建好的库函数模板， 在此模板上进行程序开发。为了能够与开发文档章节对应，将复制过来的模板文 件夹重新命名为“使用库函数点亮一个LED”。打开此文件夹，在其目录下新建 一个APP文件夹，用于存放我们开发板上所有外围器件的驱动程序，本章我们所要操作的外围器件是LED，所以在APP目录下再新建一个led文件夹用于存放我 们编写的led驱动程序，假如后面要操作开发板上的蜂鸣器，同样在APP目录下 新建一个beep文件夹用于存放蜂鸣器的驱动程序，这样做的好处是方便我们能 够快速移植代码，并且工程目录也非常清晰，为后续维护带来方便。创建的文件 夹名可自定义，不过通常使用一定意义的英文来取名，让别人看到led文件夹就 知道里面是存放驱动LED的文件。注意：本章对STM32的GPIO外设操作，需在 工程中添加stm32f10x_gpio.c和stm32f10x_rcc.c 文件，对GPIO操作的函数都 在stm32f10x_gpio.c 中，stm32f10x_gpio.h 是函数的申明及一些选项配置的宏 定义。在工程模板中这个已经添加，在后面的实验中我们就不再强调工程模板已调用的那几个文件。还需在KEIL5中把新建的APP下的led文件的路径包括进来。

 

 
LED 初始化函数

 
我们需要完成LED的驱动，所以在工程模板上新建一个led.c和led.h文件， 将其存放在led文件夹内。这两个文件内容是我们自己需要编写的，不是库文件。 通常xxx.c文件用于存放编写的驱动程序，xxx.h文件用于存放xxx.c内的stm32 头文件、管脚定义、全局变量声明、函数声明等内容。

 
因此在led.c文件内编写如下代码：

 

 
#include "led.h"

 

 
void LED_Init()

 
{

 
GPIO_InitTypeDef GPIO_InitStructure;//定义结构体变量

 

 
RCC_APB2PeriphClockCmd(LED_PORT_RCC,ENABLE);

 
GPIO_InitStructure.GPIO_Pin=LED_PIN; //选择你要设置的 IO 口

 
GPIO_InitStructure.GPIO_Mode=GPIO_Mode_Out_PP;//设置推挽输出模式

 
GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;//设置推挽输出模式

 
GPIO_Init(LED_PORT,&GPIO_InitStructure);//设置推挽输出模式

 

 
 GPIO_SetBits(LED_PORT,LED_PIN); //将 LED 端口拉高，熄灭所有LED

 
} 

 
函数中的LED_PORT_RCC、LED_PIN 和LED_PORT 是我们定义的宏，其存放在 led.h 头文件内 。 LED_PORT_RCC 定 义 的 是 LED 端口时钟 （ 如 RCC_APB2Periph_GPIOC），LED_PIN 定义的是 LED 的引脚（如 GPIO_Pin_0）， LED_PORT 定义的是LED的端口（如GPIOC）。这样定义宏的好处是有效提高了程序的移植性，即使后续需要换其他端口，只需简单修改这几个宏就可以完成对 LED 的控制。 在led.h 文件内编写如下代码：￼

 
#ifndef _led_H

 
#define _led_H

 

 
#include <stm32f10x.h>

 
/* LED时钟端口、引脚定义 */

 
#define LED_PORT GPIOC 

 
#define LED_PIN (GPIO_Pin_0|GPIO_Pin_1|GPIO_Pin_2|GPIO_Pin_3|GPIO_Pin_4|GPIO_Pin_5|GPIO_Pin_6|GPIO_Pin_7)

 
#define LED_PORT_RCC RCC_APB2Periph_GPIOC

 

 
void LED_Init(void);

 

 
#endif

 

 
LED_Init()函数就是对LED所接端口的初始化，是按照GPIO初始化步骤完成，这些内容在“寄存器点亮一个LED”章节中有介绍。下面我们主要看库函数是如何实现GPIO初始化的。 在库函数中实现GPIO的初始化函数是：

 
 void GPIO_Init(GPIO_TypeDef*GPIOx,GPIO_InitTypeDef*GPIO_InitStruct); 

 
这个函数具体有什么功能以及函数形参的意义，我们可以通过库函数帮助文档来查阅，在前面“STM32固件库介绍”章节内也讲解过如何查询库函数功能和 使用方法，这里就不多讲，不清楚的朋友可以回过头看下。 GPIO_Init 函数内有两个形参，第一个形参是GPIO_TypeDef类型的指针变量，而GPIO_TypeDef 又一个结构体类型，封装了GPIO外设的所有寄存器，所以 给它传送GPIO外设基地址即可通过指针操作寄存器内容，第一个参数值可以为 GPIOA、GPIOB、...GPIOG 等，其实这些就是封装好的GPIO外设基地址，在 stm32f10x.h 文件中可以找到。第二个形参是GPIO_InitTypeDef类型的指针变量，而GPIO_InitTypeDef 也是一个结构体类型，里面封装了GPIO外设的寄存器 配置成员。我们初始化GPIO，其实就是对这个结构体配置。

 
 如果想快速查看代码或参数可以用鼠标点击要查找的函数或者参数，然后右 键鼠标选择“Go To Definition Of ...”即可进入所要查找的函数或参数内。 假如我们要查找led.c文件中的GPIO_Init()函数，具体操作步骤如下：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-6a5a2e5a1d334996b62a52832808d936!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
查找函数内变量类型也是同样的方法，但是如果发现此方法查找不出内容，那可能就是你所查找的东西在KEIL5软件认为是不正确的。 在LED初始化函数中最开始调用的一个函数是：

 
 RCC_APB2PeriphClockCmd(LED_PORT_RCC,ENABLE); 此函数功能是使能GPIOC外设时钟，在STM32中要操作外设必须将其外设时 钟使能，否则即使其他的内容都配置好，也是徒劳无功。因为GPIO外设是挂接在APB2总线上，所以是对APB2总线时钟进行使能，函数内有两个参数，一个是用来选择外设时钟，一个是用来选择使能还是失能，使能：ENABLE，失能：DSIABLE。 在LED初始化函数内最后还调用了GPIO_SetBits(LED_PORT,LED_PIN)函数， 此函数功能是让GPIOC端口的第0-7个引脚输出高电平，让LED处于熄灭状态， 如果要对同一端口的多个引脚输出高电平，可以使用“|”运算符，相应的在对 结构体初始化配置时管脚设置那里也要使用“|”将管脚添加进去，即在led.h 文件内对LED引脚的定义。（前提条件是：要操作的多个引脚必须是配置同一种工作模式）例如：

 
GPIO_InitStructure.GPIO_Pin=GPIO_Pin_0|GPIO_Pin_1;//管脚设置 GPIO_SetBits(GPIOC,GPIO_Pin_0|GPIO_Pin_1);

 

 
其实从函数名我们大致就可以知道函数的功能。函数内有两个参数，一个是端口的选择，一个是端口管脚的选择。如果要输出低电平的话可以使用库函数 GPIO_ResetBits(GPIOC,GPIO_Pin_0); 这个函数功能和GPIO_SetBits是相反的，一个输出低电平，一个输出高电平，里面参数功能是一样的。 GPIO输出函数还有好几个，例如： 

 
void GPIO_WriteBit(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin, BitAction BitVal); 

 
void GPIO_Write(GPIO_TypeDef* GPIOx, uint16_t PortVal); 功能：设置端口管脚输出电平，这两个函数很少使用。

 

 
从GPIO内部结构可知，STM32的GPIO还可以读取输入或输出引脚电平状态 。其函数如下： 

 

 
（1）读取输入引脚 

 
uint8_t GPIO_ReadInputDataBit(GPIO_TypeDef* GPIO_Pin);

 
 功能：读取端口中的某个管脚输入电平。底层是通过读取IDR寄存器。

 
uint16_t GPIO_ReadInputData(GPIO_TypeDef* GPIOx); 功能：读取某组端口的输入电平。底层是通过读取IDR寄存器。

 

 
（2）读取输出引脚

 
uint8_t GPIO_ReadOutputDataBit(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin); 

 
功能：读取端口中的某个管脚输出电平。底层是通过读取ODR寄存器。

 
 uint16_t GPIO_ReadOutputData(GPIO_TypeDef* GPIOx); 功能：读取某组端口的输出电平。底层是通过读取ODR寄存器。

 

 
主程序

 
/***

 
使用库函数点亮一个LED

 
***/

 
#include "stm32f10x.h" // Device header

 
#include <led.h>

 

 
void ms(unsigned int t)

 
{

 
while(t--);

 
}

 
int main()

 
{

 
LED_Init();

 
while(1)

 
{

 
 GPIO_ResetBits(LED_PORT,GPIO_Pin_0);//点亮 D1

 
}

 
}

 
课后作业 

 
（1）按照上述方法点亮LED2即D2指示灯 

 
（2）实现LED闪烁 

 
（3）实现LED流水灯效果