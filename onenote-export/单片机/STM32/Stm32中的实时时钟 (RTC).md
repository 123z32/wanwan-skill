# Stm32中的实时时钟 (RTC)

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-10T09:52:14Z

Stm32中的实时时钟 (RTC)
 
 
 
 
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-1f1bba858a4d491db2ddc02f243c6f8f!1-9E53C6D99C1E5AD1!270/$value)
 
RTC的本质与定时器类似，就是一个计数器，每秒加一让其可以实现更新时间。

 

 
 
- RTC的预分配系数最高为2的20次方
 
- RTC的计数器是32位的
 
- 
RTC的时钟源可以选择以下三种

 
 
- RCC_RTCCLKSource_LSE：低速外部时钟
 
- RCC_RTCCLKSource_LSI：低速内部时钟 (通常用这个作为时钟源，32.768 kHz 进行 32768 分配可以得到 1Hz 的时钟信号)
 
- RCC_RTCCLKSource_HSE_Div128：高速外部时钟的128分频
 

 
 
- 
RTC的3个可屏蔽中断

 
 
- 闹钟中断：用来产生一个软件可编程的闹钟中断
 
- 秒中断：用来产生一个可编程的周期性中断信号(最长可达1秒)
 
- 溢出中断：指示内部可编程计数器溢出并回转为0的状态
 

 

 
 

 

 
RTC的时钟源的配置是设置 备份域控制寄存器 (RCC_BDCR) 里的 RTCSEL[1:0] 位。因此，除非备份域复位，不然此选择不能被改变。

 

 
读RTC寄存器

 

 
RTC核完全独立于RTC APB1接口。软件通过APB1接口访问RTC的预分频值、计数器值和闹钟值。但是，相关的可读寄存器只在与 RTC APB1时钟进行重新同步的RTC时钟的上升沿被更

 
新。(RTC标志也是如此的)

 

 
这意味着，如果APB1接口曾经被关闭，而读操作又是在刚刚重新开启APB1之后，则在第一次的内部寄存器更新之前，从APB1上读出的RTC寄存器数值可能被破坏了(通常读到0)。

 

 
下述几种情况下能够发生这种情形：

 

 
 
- 发生系统复位或电源复位
 
- 系统刚从待机模式唤醒
 
- 系统刚从停机模式唤醒
 

 

 

 
所有以上情况中，APB1接口被禁止时(复位、无时钟或断电)，RTC核仍保持运行状态。

 

 
因此，若在读取RTC寄存器时，RTC的APB1接口曾经处于禁止状态，则软件首先必须等待 

 
RTC_CRL寄存器中的RSF位(寄存器同步标志)被硬件置’1’。

 

 
写RTC寄存器

 

 
必须设置RTC_CRL寄存器中的CNF位，使RTC进入配置模式后，才能写入 RTC_PRL(预分频装

 
载寄存器) 、 RTC_CNT(计数器寄存器) 、 RTC_ALR(闹钟寄存器)。

 
另外，对RTC任何寄存器的写操作，都必须在前一次写操作结束后进行。可以通过查询 RTC_CR寄存器中的RTOFF状态位，判断RTC寄存器是否处于更新中。仅当RTOFF状态位是’1’ 

 
时，才可以写入RTC寄存器。

 

 
配置过程：

 

 
查询RTOFF位，直到RTOFF的值变为’1’

 
置CNF值为1，进入配置模式

 
对一个或多个RTC寄存器进行写操作

 
清除CNF标志位，退出配置模式

 
查询RTOFF，直至RTOFF位变为’1’以确认写操作已经完成。

 
仅当CNF标志位被清除时，写操作才能进行，这个过程至少需要3个RTCCLK周期。

 

 
/*

 
RTC初始化与中断

 
*/

 

 
u8 RTC_Init(void)

 
{

 
u8 temp = 0;

 
RCC_APB1PeriphClockCmd(RCC_APB1Periph_PWR | RCC_APB1Periph_BKP, ENABLE); // 使能PWR和BKP外设时钟

 
 PWR_BackupAccessCmd(ENABLE); // 取消后备区域(RTC和后备寄存器)的写保护

 
 

 
// 判断

 
 if (BKP_ReadBackupRegister(BKP_DR1) != 0x5050)

 
{

 
BKP_DeInit(); //对备份寄存器进行软件复位

 
RCC_LSEConfig(RCC_LSE_ON); //使能 外设低速晶振

 
 

 
 //检查指定的RCC标志位设置与否,等待低速晶振就绪

 
while (RCC_GetFlagStatus(RCC_FLAG_LSERDY) == RESET && temp < 250)

 
{

 
temp++;

 
delay_ms(10);

 
}

 
 

 
if (temp >= 250)

 
return 1; //超时说明初始化时钟失败,晶振有问题

 
 

 
RCC_RTCCLKConfig(RCC_RTCCLKSource_LSE); //设置 LSE 作为 RTC时钟源

 
RCC_RTCCLKCmd(ENABLE); //使能RTC时钟，要先设置时钟源

 
 

 
 RTC_WaitForSynchro(); // 等待RTC寄存器同步

 
 

 
RTC_WaitForLastTask(); // 等待最近一次对RTC寄存器的写操作完成

 
RTC_ITConfig(RTC_IT_SEC, ENABLE); // 使能RTCf的秒中断

 
 

 
RTC_WaitForLastTask(); // 等待最近一次对RTC寄存器的写操作完成

 
RTC_SetPrescaler(32767); // 设置RTC预分频的值

 
 

 
RTC_WaitForLastTask(); // 等待最近一次对RTC寄存器的写操作完成

 
RTC_SetCounter(123456); // 设置计数值(时间戳)

 
 

 
 /*

 
 实际上用不上，因为库函数封装中已经包含，不需要自己手动额外写

 
 RTC_EnterConfigMode(); // 允许配置

 
 RTC_ExitConfigMode(); // 退出配置模式

 
 */

 

 
BKP_WriteBackupRegister(BKP_DR1, 0X5050); // 向指定的后备寄存器中写入用户程序数据

 
}

 
else // 系统继续计时

 
{

 

 
RTC_WaitForSynchro(); // 等待RTC寄存器同步

 
RTC_ITConfig(RTC_IT_SEC, ENABLE); // 使能RTC秒中断

 
RTC_WaitForLastTask(); // 等待最近一次对RTC寄存器的写操作完成

 
}

 
 

 
 //初始化中断通道

 
NVIC_InitTypeDef NVIC_InitStructure;

 
NVIC_InitStructure.NVIC_IRQChannel = RTC_IRQn; // RTC全局中断

 
NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0; // 先占优先级1位,从优先级3位

 
NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0; // 先占优先级0位,从优先级4位

 
NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE; // 使能该通道中断

 
NVIC_Init(&NVIC_InitStructure); 

 
 

 
return 0;

 
}

 

 
void RTC_IRQHandler(void)

 
{

 
if (RTC_GetITStatus(RTC_IT_SEC) != RESET) // 秒钟中断

 
{

 
 RTC_WaitForSynchro(); // 等待RTC寄存器同步,读取RTC寄存器前必须做

 
 RTC_GetCounter(); // 获取当前计数值(时间戳)

 
}

 
if (RTC_GetITStatus(RTC_IT_ALR) != RESET) // 闹钟中断

 
{

 
RTC_ClearITPendingBit(RTC_IT_ALR); // 清闹钟中断

 

 
}

 
 

 
RTC_ClearITPendingBit(RTC_IT_SEC | RTC_IT_OW); // 清秒中断与溢出中断

 
RTC_WaitForLastTask();

 
}