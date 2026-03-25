# Stm32外设

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-09T10:00:15Z

Stm32外设
 
 
 
 
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-f4677bd38575410d86bec3a137602c7e!1-9E53C6D99C1E5AD1!270/$value)
 
AHB，是Advanced High performance Bus的缩写，高级高性能总线；

 
APB，是Advanced Peripheral Bus的缩写，高级外设总线。

 

 
从图中就可以看出，APB1、APB2都是AHB系统总线进行桥接出来的。另外APB1最高只有36MHz，APB2最高可以达到72MHz。

 

 
Stm32的各种外设：

 

 
IO口 (GPIO)

 
定时器 (TIM)

 
数模转换器 (DAC)

 
模数转换器 (ADC)

 
串口 (UART)

 
串行外设接口 (SPI)

 
集成电路总线 (I2C/IIC)

 
集成电路内置音频总线 (IIS/I2S)

 
外部中断/事件控制器 (EXTI)

 
通用和复用功能IO (AFIO)

 
独立看门狗 (IWDG)

 
窗口看门狗 (WWDG)

 
备份寄存器 (BKP)

 
实时时钟 (RTC) 

 
USB全速设备接口 (USB)

 
控制器局域网 (bxCAN)

 
内核外设：

 

 
嵌套中断向量控制器 (NVIC)

 
————————————————

 

 
 版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。

 
 

 
原文链接：https://blog.csdn.net/qq_40017226/article/details/130041187