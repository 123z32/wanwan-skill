# GPIO八种工作方式

> 来源: OneNote > 单片机 > 单片机
> 修改: 2025-04-07T11:55:49Z

GPIO八种工作方式
 
 
 
 
 

 
上拉输入模式

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-2b944168ffdd05eb21b526550817327f!1-9E53C6D99C1E5AD1!se4bfe7dee5fb41d7ad3690f0d6524a94/$value)
 
默认情况下输入引脚数据为1，高电平。

 

 
上拉输入模式下，I/O端口的电平信号直接进入输入数据寄存器。但是在I/O端口悬空（在无信号输入）的情况下，输入端的电平保持在高电平（自己理解：上拉电阻连接电压）；并且在I/O端口输入为低电平的时候，输入端的电平也是低电平（自己理解：上拉电阻上的电压和端口导通）。

 

 
施密特触发器：施密特就是为了防止在某一个临界电平的情况出现各种情况的抖动出现，为了稳定我们的输出而设计的。

 
施密特触发器采用电位触发方式，其状态由输入信号电位维持；对于负向递减和正向递增两种不同变化方向的输入信号，施密特触发器有不同的阈值电压。

 

 
下拉输入模式

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-d2f960dc507f0a182af40234c005ae03!1-9E53C6D99C1E5AD1!se4bfe7dee5fb41d7ad3690f0d6524a94/$value)
 
默认情况下输入引脚为0，低电平。

 
下拉输入模式下，I/O端口的电平信号直接进入输入数据寄存器。但是在I/O端口悬空（在无信号输入）的情况下，输入端的电平保持在低电平；并且在I/O端口输入为高电平的时候，输入端的电平也是高电平。

 
浮空输入模式

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-eeb041a5694b0d672c1fa63ba55e4ff0!1-9E53C6D99C1E5AD1!se4bfe7dee5fb41d7ad3690f0d6524a94/$value)
 
浮空输入模式下，I/O端口的电平信号直接进入输入数据寄存器。也就是说，I/O的电平状态是不确定的，完全由外部输入决定；如果在该引脚悬空（在无信号输入）的情况下，读取该端口的电平是不确定的。

 
通常用于IIC、USART。

 
模拟输入模式

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-97b09440c2c30b692b49df5f55e23e95!1-9E53C6D99C1E5AD1!se4bfe7dee5fb41d7ad3690f0d6524a94/$value)
 
模拟输入模式下，I/O端口的模拟信号（电压信号，而非电平信号）直接模拟输入到片上外设模块，比如ADC模块等。模拟信号一般：3.3v 5v 9v。

 
开漏输出模式

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-92133a1572d00f7801fdaac44ed88463!1-9E53C6D99C1E5AD1!se4bfe7dee5fb41d7ad3690f0d6524a94/$value)
 ![在这里插入图片描述](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-c51cf099edf307ee32133f3cf38b9462!1-9E53C6D99C1E5AD1!se4bfe7dee5fb41d7ad3690f0d6524a94/$value)
 
可以输出0和1，适用于电平不匹配场合，要得到高电平需要上拉电阻才行。

 

 
开漏输出模式下（上拉电阻+N-MOS管），通过设置位设置/清除寄存器或者输出数据寄存器的值，途经N-MOS管，最终输出到I/O端口。这里要注意N-MOS管，当设置输出的值为高电平的时候，N-MOS管处于关闭状态，此时I/O端口的电平就不会由输出的高低电平决定，而是由I/O端口外部的上拉或者下拉决定；当设置输出的值为低电平的时候，N-MOS管处于开启状态，此时I/O端口的电平就是低电平。同时，I/O端口的电平也可以通过输入电路进行读取；注意，I/O端口的电平不一定是输出的电平。

 
开漏复用输出模式

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-1544c0e34e6f00730af704f0097dcc93!1-9E53C6D99C1E5AD1!se4bfe7dee5fb41d7ad3690f0d6524a94/$value)
 
开漏复用输出模式，与开漏输出模式很是类似。只是输出的高低电平的来源，不是让CPU直接写输出数据寄存器，取而代之利用片上外设模块的复用功能输出来决定的。

 
片内外设功能：TX1，MOSI，MISO，SCK，SS

 
推挽输出模式

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-94e8fe35628c07a738350d241da00749!1-9E53C6D99C1E5AD1!se4bfe7dee5fb41d7ad3690f0d6524a94/$value)
 ![在这里插入图片描述](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-1de63dbf3e9106443e27541222904e3d!1-9E53C6D99C1E5AD1!se4bfe7dee5fb41d7ad3690f0d6524a94/$value)
 
可以输出高低电平0和1，适用于双向IO使用。

 

 
推挽输出模式下（P-MOS管+N-MOS管），通过设置位设置/清除寄存器或者输出数据寄存器的值，途经P-MOS管和N-MOS管，最终输出到I/O端口。这里要注意P-MOS管和N-MOS管，当设置输出的值为高电平的时候，P-MOS管处于开启状态，N-MOS管处于关闭状态，此时I/O端口的电平就由P-MOS管决定：高电平；当设置输出的值为低电平的时候，P-MOS管处于关闭状态，N-MOS管处于开启状态，此时I/O端口的电平就由N-MOS管决定：低电平。同时，I/O端口的电平也可以通过输入电路进行读取；注意，此时I/O端口的电平一定是输出的电平。

 

 
推挽复用输出模式

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-17af8a0874b002240ecc01af64384856!1-9E53C6D99C1E5AD1!se4bfe7dee5fb41d7ad3690f0d6524a94/$value)
 
挽复用输出模式，与推挽输出模式很是类似。只是输出的高低电平的来源，不是让CPU直接写输出数据寄存器，取而代之利用片上外设模块的复用功能输出来决定的。

 
片内外设功能IIC的SCL、SDL