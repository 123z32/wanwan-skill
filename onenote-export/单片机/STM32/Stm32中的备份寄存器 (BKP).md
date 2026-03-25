# Stm32中的备份寄存器 (BKP)

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-09T11:12:19Z

Stm32中的备份寄存器 (BKP)
 
 
 
 
 

 
备份寄存器拥有以下特性

 

 
 
- 当VDD电源被切断，他们仍然由VBAT维持供电。
 
- 20字节数据后备寄存器(中容量和小容量产品)，或84字节(42*16 Bit)数据后备寄存器(大容量和互联型产品)
 
- 当系统在待机模式下被唤醒，或系统复位或电源复位时，他们也不会被复位。
 
- BKP寄存器是16位的可寻址寄存器，可以用半字(16位)或字(32位)的方式操作这些外设寄存器。
 

 

 
备份寄存器的复位

 
 
- 软件复位，备份区域复位可由设置备份域控制寄存器 (RCC_BDCR)中的 BDRST位产生
 
- 在VDD和VBAT两者都掉电的情况下，VDD或VBAT上电将引发备份区域复位。
 

 

 
后备区域的保护

 

 
在复位之后，对后备区域(备份寄存器和RTC) 的访问将被禁止，后备区域被保护以防止可

 
能存在的意外的写操作。

 
需要执行以下操作可以使能对后备区域的访问。

 

 
1.通过设置寄存器 RCC_APB1ENR 的 PWREN 和 BKPEN 位来打开电源和后备接口的时钟

 
说人话就是使能 电源控制 (PWR) 与 备份寄存器 (BKP)的时钟

 
2.电源控制寄存器(PWR_CR)的DBP位来使能对后备寄存器和RTC的访问

 

 

 

 
/*

 
BKP寄存器基础操作示例

 
*/

 

 
RCC_APB1PeriphClockCmd(RCC_APB1Periph_PWR | RCC_APB1Periph_BKP, ENABLE); //使能PWR和BKP外设时钟

 

 
BKP_ReadBackupRegister(BKP_DR1) //读取 BKP_DR1 寄存器，启用时钟后就可以读取了

 
BKP_DeInit() //对备份寄存器进行软件复位

 
 

 

 
PWR_BackupAccessCmd(ENABLE); //取消后备区域的写保护，但如果RTC的时钟是HSE/128，无法进行写保护。

 
BKP_WriteBackupRegister(BKP_DR1, 0X5050); //向 BKP_DR1 寄存器写 0x5050，写之前要取消写保护才可以