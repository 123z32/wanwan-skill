# Stm32的端口复用与重映射

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-09T10:11:22Z

Stm32的端口复用与重映射
 
 
 
 
 

 

 
Stm32有很多的IO口，同时有很多的外设。这些IO口默认是用来做普通的输出输入引脚，而配置为外设需要用到IO口，就叫IO口的复用。如：

 
 

 | 
管脚名称 

 

 
 | 主功能 (复位后)
 | 默认复用功能
 | 重定义功能
 
 

 | PA9
 | PA9
 | USART1_TX
 | 无
 
 

 | PA10
 | PA10
 | USART1_RX
 | 无
 
 

 
/*

 
以下代码则是配置PA9、PA10为复用。

 
其实PA10作为输入引脚，并不区分复用不复用的，因为输出只能有一个外设控制，

 
但是输入可以多个外设读取，不冲突。

 
*/

 

 
//需要使能GPIO和复用外设的时钟，使用默认复用功能时，AFIO时钟不需要使能

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1, ENABLE);

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

 

 
//初始化TX引脚 PA9 为复用推挽输出 

 
GPIO_InitTypeDef GPIO_InitStructure;

 
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP; //复用推挽输出

 
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;

 
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;

 
GPIO_Init(GPIOA, &GPIO_InitStructure);

 

 
//初始化RX引脚 PA10 为上拉输入

 
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;

 
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;

 
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;

 
GPIO_Init(GPIOA, &GPIO_InitStructure);

 

 
每个内置外设都有若干个输入输出引脚，一般这些引脚的输出端口都是固定不变的。但在实际使用中，为了让设计工程师可以更好地安排引脚的走向和功能，在Stm32中引入了外设引脚重映射的概念。即一个外设的引脚除了具有默认的端口外，还可以通过设置重映射

 
寄存器的方式，把这个外设的引脚映射到其它的端口。

 

 
 

 | 
管脚名称 

 

 
 | 主功能 (复位后)
 | 默认复用功能
 | 重定义功能
 
 

 | PB6
 | PB6
 | 1I2C1_SCL / TIM4_CH1
 | USART1_TX
 
 

 | PB7
 | PB7
 | I2C1_SDA / FSMC_NADV / TIM4_CH2
 | USART1_RX
 
 

 

 
如 外设的 USART1_TX 引脚除了PA9外，还可以使用PB6。

 

 
//使能重映射之后的GPIO时钟

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);

 
//使能复用外设的时钟

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1, ENABLE);

 
//重映射需要使能AFIO时钟，因为下一行代码是配置AFIO_MAPR寄存器

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);

 

 
//实际上是对AFIO进行操作：重映射引脚

 
GPIO_PinRemapConfig(GPIO_Remap_USART1, ENABLE);

 

 
//初始化PB6与PB7引脚，略

 
//...

 

 
部分重映射&完全重映射

 
部分重映射：功能外设的部分引脚重新映射，还有一部分引脚是原来的默认引脚

 
完全重映射：功能外设的所有引脚都重新映射

 

 
何时需要使能AFIO时钟？

 
根据手册说明：对寄存器AFIO_EVCR(事件控制寄存器)、AFIO_MAPR(复用重映射和调试I/O配置寄存器)和AFIO_EXTICRX(外部中断配置寄存器) 进行读写操作前，应当首先打开AFIO 的

 
时钟。

 

 
说人话就是在用到 外部中断 和 端口重映射 的时候要使能AFIO时钟