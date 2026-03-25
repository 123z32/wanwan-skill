# Stm32的外部中断 (EXTI)

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-09T10:30:11Z

Stm32的外部中断 (EXTI)
 
 
 
 
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-918c3e49ab764f118db0fadd759c45b1!1-9E53C6D99C1E5AD1!270/$value)
 

 

 
/*

 
配置外部中断的示例代码

 
*/

 
void EXTI(void)

 
{

 
 //使能GPIOA时钟

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

 
 //因为使用到了AFIO的中断引脚选择功能，所以要使能AFIO的时钟

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);

 

 
GPIO_InitTypeDef GPIO_InitStructure;

 
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;

 
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_14;

 
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;

 
GPIO_Init(GPIOA, &GPIO_InitStructure);

 

 
 //实际上是对AFIO进行操作：将PA14信号输出至EXTI的14号线

 
GPIO_EXTILineConfig(GPIO_PortSourceGPIOA, GPIO_PinSource14);

 

 
 //初始化EXTI

 
EXTI_InitTypeDef EXTI_InitStructure;

 
EXTI_InitStructure.EXTI_Line = EXTI_Line14;

 
EXTI_InitStructure.EXTI_LineCmd = ENABLE;

 
EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt; //使用中断

 
EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Falling; //下降沿触发

 
EXTI_Init(&EXTI_InitStructure);

 
 

 
//设置优先级分配配置

 
NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);

 

 
 //配置外部中断

 
NVIC_InitTypeDef NVIC_InitStructure;

 
NVIC_InitStructure.NVIC_IRQChannel = EXTI15_10_IRQn;

 
NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;

 
NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;

 
NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;

 
NVIC_Init(&NVIC_InitStructure);

 
}

 

 

 
//中断函数

 
void EXTI15_10_IRQHandler(void)

 
{

 
if (EXTI_GetITStatus(EXTI_Line14) == SET)

 
{

 

 
 

 
 //清除中断标志位

 
EXTI_ClearITPendingBit(EXTI_Line14);

 
}

 
}