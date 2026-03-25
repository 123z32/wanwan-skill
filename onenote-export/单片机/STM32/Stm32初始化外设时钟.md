# Stm32初始化外设时钟

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-07T01:29:46Z

Stm32初始化外设时钟
 
 
 
 
 

 
每个外设都有独立时钟，如果不打开时钟外设就不能用，原因就是为了低功耗节省用电，不用的外设可以不打开时钟

 
开启外设时钟的方法：

 

 
/*

 
AHB外设总线：

 
DMA1,DMA2,SRAM,FLITF,CRC,FSMC,SDIO

 
*/

 
RCC_AHBPeriphClockCmd(RCC_AHBPeriph_CRC,ENABLE);

 
RCC_AHBPeriphClockCmd(RCC_AHBPeriph_CRC,DISABLE);

 

 
/*

 
APB1外设总线：

 
TIM2,TIM3,TIM4,TIM5,TIM6,TIM7,TIM12,TIM13,TIM14,WWDG

 
SPI2,SPI3,USART2,USART3,UART4,UART5,I2C1,I2C2,USB,CAN1,CAN2,BKP,PWR,DAC,CEC,

 
*/

 
RCC_APB1PeriphClockCmd(RCC_APB1Periph_SPI2,ENABLE);

 
RCC_APB1PeriphClockCmd(RCC_APB1Periph_SPI2,DISABLE);

 

 
/*

 
APB2外设总线：

 
 AFIO,GPIOA,GPIOB,GPIOC,GPIOD,GPIOE,GPIOF,GPIOG,ADC1,ADC2

 
 TIM1,SPI1,TIM8,USART1,ADC3,TIM15,TIM16,TIM17,TIM9,TIM10,TIM11

 
*/

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, DISABLE);