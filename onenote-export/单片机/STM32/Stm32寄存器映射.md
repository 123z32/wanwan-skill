# Stm32寄存器映射

> 来源: OneNote > 单片机 > STM32
> 修改: 2025-01-23T09:51:20Z

Stm32寄存器映射
 
 
 
 
 

 
以最简单的GPIO讲，将 GPIOA 相关的固件库代码拿出来变很容易明白。

 

 
#define PERIPH_BASE ((uint32_t)0x40000000) //外设基地址

 
#define APB2PERIPH_BASE (PERIPH_BASE + 0x10000) //APB2总线基地址

 
#define GPIOA_BASE (APB2PERIPH_BASE + 0x0800) //GPIOA 基地址

 

 
typedef struct

 
{

 
 __IO uint32_t CRL;

 
 __IO uint32_t CRH;

 
 __IO uint32_t IDR;

 
 __IO uint32_t ODR;

 
 __IO uint32_t BSRR;

 
 __IO uint32_t BRR;

 
 __IO uint32_t LCKR;

 
} GPIO_TypeDef;

 

 
#define GPIOA ((GPIO_TypeDef *) GPIOA_BASE) //GPIOA结构

 

 
很明显可以看出来，固件库代码的条理非常清晰，而且非常巧妙。除了第一个外设基地址是固定值，其他的基地址都是通过 上一级基地址+偏移 计算出来的，最后GPIOA是一个 指

 
定地址强制转换结构。

 
这样我们如果想要操作寄存器，则可以用

 

 
GPIOA->CRL&=0xFF0FFFFF; //将寄存器 20~23位 置0

 
GPIOA->CRL|=0x00300000; //设置寄存器 20~23位，实际作用是设置PA5为推挽输出

 
GPIOA->ODR|=1<<5; //PA5 输出高电平

 

 
另外可以注意到，所有地址都是使用了#define定义常量值，这是因为编译器在进行项目编

 
译的时候，对于常量间的计算，是能直接优化成常量值。如：

 

 
GPIOA->CRL&=0xFF0FFFFF;

 
//进行预编译处理之后为:

 
((GPIO_TypeDef *) ((((uint32_t)0x40000000) + 0x10000) + 0x0800))&=0xFF0FFFFF;

 
//然后优化为:

 
((GPIO_TypeDef *) ((uint32_t)0x40010800) &=0xFF0FFFFF;