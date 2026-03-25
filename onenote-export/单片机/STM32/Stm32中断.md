# Stm32中断

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-09T10:19:05Z

Stm32中断
 
 
 
 
 

 

 
Stm32F103xx 中有60个可编程外设中断。配置中断的代码如下：

 

 
抢占优先级：优先级高的能打断优先级低

 
响应优先级：当抢占优先级相同时，响应优先级高的先执行

 

 
注意：优先级的值越小，优先级越高(越先执行)

 

 
总结：抢占优先级高的可以中断嵌套，响应优先级高的可以优先排队，抢占优先级和响应优先级均相同的按中断号排队

 

 
可能有些朋友没办法理解响应优先级的优先排队的作用，那我再解释一下优先排队的概念：

 

 
假设一个[抢占优先级=0]的中断①进行过程中，先触发了[抢占优先级=1,响应优先级=2]的中断②，再触发了[抢占优先级=1,响应优先级=1]的中断③

 

 
则中断①结束后，理论上应该按照先来后到先执行中断②，然后再执行中断③的，但实际上因为中断③响应优先级更高，因此中断③拥有优先排队(插队)的权限，因此最终是先执行中断③，再执行中断②

 

 
初始化中断

 

 
#define NVIC_PriorityGroup_0 ((uint32_t)0x700) // 0位抢先优先级、4位响应优先级

 
#define NVIC_PriorityGroup_1 ((uint32_t)0x600) // 1位抢先优先级、3位响应优先级

 
#define NVIC_PriorityGroup_2 ((uint32_t)0x500) // 2位抢先优先级、2位响应优先级

 
#define NVIC_PriorityGroup_3 ((uint32_t)0x400) // 3位抢先优先级、1位响应优先级

 
#define NVIC_PriorityGroup_4 ((uint32_t)0x300) // 4位抢先优先级、0位响应优先级

 

 
NVIC_PriorityGroupConfig (NVIC_PriorityGroup_2); //设置优先级分配配置

 

 
NVIC_InitTypeDef NVIC_InitStructure;

 
NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn; //设置中断通道类型

 
NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE; //设置中断使能

 
/*优先级的值越小，优先级越高(越先执行)*/

 
NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1; //设置抢占优先级 

 
NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1; //设置响应优先级

 

 
NVIC_Init(&NVIC_InitStructure); //初始化中断通道