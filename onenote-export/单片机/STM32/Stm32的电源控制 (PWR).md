# Stm32的电源控制 (PWR)

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-09T10:58:01Z

Stm32的电源控制 (PWR)
 
 
 
 
 

 

 
Stm32的工作电压(VDD)为2.0～3.6V。通过内置的电压调节器提供所需的1.8V电源。 当主电源VDD掉电后，通过VBAT脚为实时时钟(RTC)和备份寄存器提供电源。实际上，VBAT脚还可以为 LSE振荡器 和 PC13~PC15 端口供电，可以保证当主电源被切断时RTC能继续工作。但当使用VBAT供电时，PC13~PC15无法用作GPIO。

 

 
 

 | 管脚名称
 | 主功能 (复位后默认)
 | 复用功能
 | 功能
 
 

 | PC13
 | PC13
 | TAMPER / RTC
 | 用于侵入检测，RTC校准时钟、RTC闹钟或秒输出
 
 

 | PC14
 | PC14
 | OSC32_IN
 | LSE引脚
 
 

 | PC15
 | PC15
 | OSC32_OUT
 | LSE引脚
 
 

 
 

 
一般来说，VBAT脚接一个纽扣电池供电，如正点原子的开发板。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-85809553e2ea473fa1775e35b1e4ae05!1-9E53C6D99C1E5AD1!270/$value)
 

 
从图中可以看出来，除了上面说到的之外，RCC_BDCR 寄存器也在后备供电区域内。但实际上，RCC_BDCR 寄存器只有 LSEON (外部低速振荡器使能)、LSEBYP (外部低速时钟振荡器旁路)、RTCSEL (RTC时钟源选择) 和 RTCEN (RTC时钟使能)位处于备份域。另外的 LSERDY (外

 
部低速LSE就绪) 与 BDRST (备份域软件复位) 不处于备份域，因为没有必要。