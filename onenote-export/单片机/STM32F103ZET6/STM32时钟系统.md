# STM32时钟系统

> 来源: OneNote > 单片机 > STM32F103ZET6
> 修改: 2025-02-14T13:41:05Z

STM32时钟系统
 
 
 
 
 

 
本章将向大家介绍STM32的时钟系统，重点分析时钟树，只要理解好时钟树， STM32 一切时钟的来龙去脉会非常清楚。通过介绍STM32时钟配置过程，让大家 学会如何修改系统时钟频率，本章最后通过一个简单的LED闪烁程序来讲述如何 自定义系统时钟。学习本章可以参考“STM32F10x中文参考手册”“复位和时钟 控制（RCC）”章节内容，若结合视频学习效果更佳。本章分为如下几部分内容：

 
11.1 STM32 时钟树

 
11.2 时钟配置函数 

 
11.3 自定义系统时钟 

 
11.4 实验现象

 

 
11.1 STM32 时钟树 

 
时钟对于单片机来说是非常重要的，它为单片机工作提供一个稳定的机器周期从而使系统能够正常运行。时钟系统犹如人的心脏，一旦有问题整个系统就崩溃。我们知道STM32属于高级单片机，其内部有很多的外设，但不是所有外设都使用同一时钟频率工作，比如内部看门狗和RTC，它只需30几KHz的时钟频率即可工作，所以内部时钟源就有多种选择。

 
在前面章节的介绍中，我们知道STM32 系统复位后首先进入SystemInit函数进行时钟的设置，将STM32F1系统时钟设置为72MHz（我们开发板上使用的STM32F103ZET6最大可达到72M（超频除外））， 然后进入主函数。那么这个系统时钟大小如何得来，其他外设的时钟又如何划分， 这些问题都可以通过一张时钟树图找到答案，只要理解好时钟树，STM32一切时钟的来龙去脉就会非常清楚。下面就来了解下时钟树，如图11.1.1所示，我们 把时钟树拆分逐个介绍。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-b05d879862714b4caf2a75fb3abbbce8!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
在STM32 时钟系统中，有5个重要的时钟源，分别是LSI、LSE、HSI、HSE、 PLL。按照时钟频率分可分为高速时钟源和低速时钟源，在这 5 个中 HSI，HSE 以 及 PLL 属于高速时钟，LSI 和 LSE 属于低速时钟。按照时钟来源可分为外部时 钟源和内部时钟源，外部时钟源就是在STM32晶振管脚处接入外部晶振的方式获 取时钟源，其中HSE和LSE是外部时钟源，其他的是内部时钟源。下面我们就按 照上图中数字顺序来介绍。 

 
（1）图标1 HSI是内部高速时钟，RC振荡器，频率为8MHz。可作为系统时钟或PLL锁相环的输入。

 
（2）图标2 HSE是外部高速时钟，芯片的23和24引脚即为外部高速晶振管脚。可通过外接一个频率范围是4-16MHz的时钟或者晶振，我们开发板上接的是一个8MHz的外部晶振。HSE可以作为系统时钟和PLL锁相环输入，还可以经过128分频后输入给RTC。 

 
（3）图标3 LSI是内部低速时钟，RC振荡器，频率大约为40K，可供独立看门狗和RTC使用，并且独立看门狗只能使用LSI时钟。 

 
（4）图标4LSE是外部低速时钟，我们开发板上STM32芯片的PC14和PC15 即为外部低速时钟管脚。通常在此管脚上外接一个32.768KHz的晶振，

 
图标5PLL是锁相环，用于倍频输出，因为开发板外部高速晶振也只有8M， 而我们这块芯片的最大时钟频率是72M，因此可通过PLL锁相环来倍频。从图标 5 中可以看到，PLL时钟输入源可选择为HSI/2、HSE或者HSE/2，时钟源经过2-16 倍频后输入给PLLCLK，如果系统时钟选择由PLLCLK提供，则PLLCLK最大值不要超过72M。 

 
那么它是怎么倍频产生72MHz系统时钟的呢？我们看到在主PLL内有倍频器和分频器，如图11.1.2所示。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-1401e4e6c9504a3d8fcacdffff4a6359!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
从图11.1.2可以看出，PLL时钟源的输入信号要先经过一个PLLMUL倍频器， 将HSE或HSI倍频（2-16）后输入给PLLCLK，如果系统时钟源SYSCLK选择PLLCLK作为它的来源，则最大值不能超过72M。虽然可以做超频处理，但会打破系统的稳定性，这个是不划算的。假如PLLSRC的时钟来源由HSE提供，我们开发板使用的HSE是8M晶振，经过PLLMUL 9倍频后可以输出72M时钟频率给PLLCLK。 总结：如果我们选择HSE是PLL的时钟源，PLL是SYSCLK的时钟源，即SYSCLK为72MHz，这个也是我们库函数模板中SystemInit所配置的最终系统时钟。

 
 上面我们简单介绍了下STM32的5个时钟源，那么它们是怎么给其他外设和系统提供时钟的呢？在上图11.1.1时钟树图中我们把常用的时钟用字母框起 

 
（A）MCO是STM32 的一个时钟输出IO(PA8)，它可以选择一个时钟信号输出，可以选择为 PLL 输出的 2 分频、 HSI、 HSE或者系统时钟。这个时钟可以用来给外部其他系统提供时钟源。

 
（B）RTC时钟。从图中线的流向可知，RTC时钟来源可以是内部低速的LSI时钟，外部低速LSE时钟（32.768K），还可以通过HSE 128分频后得到。 

 
（C）USB 时钟。STM32 中有一个全速功能的 USB 模块，其串行接口引擎需要一个频率为 48MHz 的时钟源，该时钟源只能从 PLL 输出端获取，可以选择为 1.5 分频或者 1 分频，也就是当需要使用 USB模块时，PLL 必须使能，并且 PLLCLK 时钟频率配置为 48MHz 或 72MHz。 

 
（D）SYSCLK系统时钟。它是 STM32 中绝大部分部件工作的时钟源。它的时钟来源可以由HSI、HSE、PLLCLK提供，相信大家选择STM32F1这种高级芯片， 都希望有一个比较大的时钟频率，因此选择PLLCLK作为系统时钟。PLLCLK又是从HSE或HSI经过PLL倍频得到。根据前面PLL计算关系大家就可以算出系统时钟是多少。 

 
（E）其他所有外设。从时钟图上可以看出，其他所有外设的时钟最终来源 都是 SYSCLK。SYSCLK 通过 AHB 分频器分频后送给各模块使用。这些模块包括：

 
①、 AHB 总线、内核、内存和 DMA 使用的 HCLK 时钟。 

 
②、通过 8 分频后送给 Cortex 系统定时器时钟，即SysTick。 ③、直接送给 Cortex 的空闲运行时钟 FCLK。

 
④、送给 APB1 分频器。 APB1 分频器输出一路供 APB1 外设使用(PCLK1， 最大频率 36MHz)，另一路送给定时器(Timer)1、2倍频使用。 

 
⑤、送给 APB2 分频器。 APB2 分频器分频输出一路供 APB2 外设使用 (PCLK2，最大频率 72MHz)，另一路送给定时器(Timer)1 倍频器使用。 

 
⑥、送给ADC分频器。ADC分频器经过2、4、6、8分频后送给ADC1/2/3使用，ADC最大频率为14M。 

 
⑦、二分频后送给SDIO使用。 

 
其中需要理解的是 APB1 和 APB2 的区别，APB1 上面连接的是低速外设，包括电源接口、备份接口、CAN、USB、I2C1、I2C2、UART2、UART3 等，APB2 上面连接的是高速外设包括 UART1、 SPI1、 Timer1、 ADC1、 ADC2、GPIO等。 大家可以简单这样记忆：2>1，所以APB2的速度大于APB1的速度。 在时钟树图中我们还可以得到一个重要信息，大多数有关时钟输出部分都有一个使能控制，比如AHB总线、APB1外设、APB2外设、内核时钟等。当需要使用某个时钟的时候一定要开启它的使能，否则将不工作。在前面我们介绍库函数 点亮一个LED实验的时候就使能了GPIO的外设时钟，如果不开启，LED将不工作。

 

 
11.2 时钟配置函数

 
时钟初始化配置函数在前面章节的介绍中，我们知道STM32系统复位后首先进入SystemInit函数进行时钟的设置，然后进入主函数main。那么我们就来看下SystemInit()函数到底做了哪些操作，首先打开我们前面使用库函数编写的LED程序，在system_stm32f10x.c 文件中可以找到SystemInit()函数，如果不想找的可以直接打开其头文件，通过前面教大家的快速进入函数的方法进入到SystemInit() 内。SystemInit()代码如下：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-8276c8397eb84766be634487e9de5dcf!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-37fd59e9f48042aba4ff4f57bac7ee08!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-7b2a16c64fc648b4ac4fa8c52e5acbe7!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
SystemInit 函数开始通过条件编译，先复位RCC寄存器，同时通过设置 CR 寄存器的 HSI 时钟使能位来打开 HSI 时钟。默认情况下如果 CR 寄存器复位，是选择HSI作为系统时钟，这点大家可以查看 RCC->CR寄存器相关位描述可以得知，当低两位配置为00的时候（复位之后），会选择 HSI振荡器为系统时钟。也就是说，调用 SystemInit 函数之后，首先是选择HSI作为系统时钟。 在设置完相关寄存器后才换成HSE作为系统时钟，接下来SystemInit函数内部会调用 SetSysClock()函数。这个函数内部是根据宏定义设置系统时钟频率。函数如下：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-dafb185c75094d44a2654cbe9df2816f!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
}

 

 
在system_stm32f10x.c 文件的开头就有对此宏定义，系统默认的宏定义是 72MHz，如下：

 
#define SYSCLK_FREQ_72MHz 72000000

 
如果你要设置为 36MHz，只需要注释掉上面代码，然后加入下面代码即可：

 
#define SYSCLK_FREQ_36MHz 36000000

 
根据该函数内部实现过程可知，直接调用SetSysClockTo72()函数，此函数功能是将系统时钟SYSCLK设置为72M，AHB总线时钟设置为72M，APB2总线时钟 设置为72M，APB1总线时钟设置为36M，PLL时钟设置为72M。函数具体实现大 家可以打开库函数查看，这里我们就不截取出来。如果SystemInit内实现过程 看不懂没有关系，大家只要知道SystemInit函数执行完，时钟大小设置如下：

 
 SYSCLK（系统时钟） =72MHz

 
 AHB 总线时钟(HCLK=SYSCLK) =72MHz

 
 APB1 总线时钟(PCLK1=SYSCLK/2) =36MHz

 
 APB2 总线时钟(PCLK2=SYSCLK/1) =72MHz

 
 PLL 主时钟 =72MHz

 
 这些时钟值大家要记住。

 

 
11.2.2 时钟使能配置函数

 
 上一节我们说到，当使用一个外设时，必须先使能它的时钟。那么怎么通过库函数使能时钟呢？如需了解寄存器配置时钟，可以参考《STM32F10x中文参考手册》“复位和时钟控制（RCC）”章节内容，里面有详细寄存器的介绍。固件 库已经把时钟相关寄存器的使能配置都封装好，放在stm32f10x_rcc.c 和 stm32f10x_rcc.h 中。只需要打开stm32f10x_rcc.h 文件，会发现有很多的宏定义和时钟使能函数的声明。这些时钟函数可大致分为三类。一类是外设时钟使能函数，一类是时钟源和倍频因子配置函数，还有一类是外设复位函数。当然还有几个获取时钟源配置的函数。下面就来简单介绍下这些函数的使用。

 
 首先我们看下时钟使能函数，时钟使能函数包括外设时钟使能和时钟源使能。首先我们看下外设时钟使能相关函数，如下：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-8321e7e59c6a410da62615c548794fda!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
上面3个时钟使能函数也正是STM32的3条总线（这个在前面介绍存储器与 寄存器章节讲过）。由于STM32的外设都是挂接在AHB和APB总线上的，所以要使能外设时钟，也就是使能对应外设所挂接的总线时钟。比如GPIO外设它是挂接在APB2总线上的，如果使用GPIO外设，就需要先调用

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-bc1abce4bbd2474b964b88b000b37e3d!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
函数使能APB2时钟。有的朋友就会问：我怎么知道哪个外设挂接在哪个总线上呢？很简单，可以通过STM32中文参考手册查找，还可以在固件库 stm32f10x_rcc.h 文件中查找。其实这些知识在存储器与寄存器章节已经介绍，大家回过头看下即可。

 
外设时钟使能函数有两个形参，第一个是你所使用的外设所挂接的时钟，第 二个是选择你用的外设时钟使能还是失能。比如我们要使能端口GPIOC，那么第 一个传递的参数是：RCC_APB2Periph_GPIOC宏，第二个传递的参数是ENABLE使 能。从第一个参数名来看也非常好理解，RCC表示复位和时钟控制器，APB2表示 GPIOC 是挂接在APB2总线上，Periph表示外设，后面的GPIOC表示我们使能的 是GPIOC 端口。第二个参数ENABLE表示使能。假如使能GPIOA端口时钟，那么 只需要修改第一个参数值即可，按照刚才介绍的名意义，可以无需查找即可写出 RCC_APB2Periph_GPIOA。其他的外设初始化方法类似。 下面我们介绍下时钟源使能函数，通过前面的讲解，知道STM32有5大类时 钟源，这里我们只挑几个重要的时钟源使能函数介绍，如下：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-ad7df33474a942db8b8788080e22ea16!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
这些函数都是用来使能相应的时钟源，比如我们要使能PLL时钟，那么就调 用RCC_PLLCmd 函数，函数有一个形参，和前面外设时钟的第二个参数一样，如果为ENABLE表示使能，DISABLE表示失能。

 

 
我们再来介绍下另外一类时钟函数——时钟源和倍频因子配置函数。这类函数主要用来选择相应的时钟源和配置时钟倍频因子，比如系统时钟，它可以由 HSE、HSI或者PLLCLK作为它的时钟源，具体选择哪个，就是通过时钟源配置函数实现。比如我们设置HSE作为系统时钟源，那么调用的函数就是： RCC_SYSCLKConfig(RCC_SYSCLKSource_HSE);//配置时钟源为 HSE

 

 
在前面也介绍了APB1的时钟频率是HCLK的2分频。那么可以调用下面这个函数来实现：

 
RCC_PCLK1Config(RCC_HCLK_Div2);//设置低速 APB1 时钟（PCLK1） 时钟倍频因子配置函数主要用来修改系统的时钟频率。在本章最后一节我们会通过一个简单LED闪烁程序来说明修改倍频因子后时钟的变化。

 
最后介绍下另外一类时钟函数——外设复位函数。其函数如下：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-008d72c3c0a8454794cc6cb1949ec71a!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
在STM32F10x高容量的芯片中没有RCC_AHBPeriphResetCmd函数。这类函数与前面讲解的外设时钟使能函数用法一样，只不过外设时钟使能函数是用于使能外设时钟，而这类函数是用于外设复位，从函数名也可以区分出来。

 

 
11.3 自定义系统时钟 

 
在时钟树的讲解中我们知道，通过修改PLLMUL中的倍系数值（2-16）可以改变系统的时钟频率。在库函数中也有对时钟倍频因子配置的函数，如下： 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-1498f6113cf447dda8d7d095b4807803!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
第一个参数是PLL时钟源选择，我们例程中采用的都是HSE作为PLL的时钟源，可以设置为RCC_PLLSource_HSE_Div1/RCC_PLLSource_HSE_Div2。第二个参数就是倍频因子值（RCC_PLLMul_2~RCC_PLLMul_16）。 为了方便朋友们能够修改系统时钟，我们这里自定义一个系统时钟初始化函数，我们将函数放在对应实验程序的main.c中。具体代码如下：

 
/**************************************************************************

 
 *****

 
 * 函 数 名

 
* 函数功能

 
钟调整

 
: RCC_HSE_Config

 
 : 自定义系统时钟，可以通过修改PLL时钟源和倍频系数实现时

 
* 输 入 :div：RCC_PLLSource_HSE_Div1/RCC_PLLSource_HSE_Div2

 
 pllm：RCC_PLLMul_2-RCC_PLLMul_16

 
 * 输 出 :无

 
***************************************************************************

 
 ****/

 
 void RCC_HSE_Config(u32 div,u32 pllm) //自定义系统时间（可以修改时钟）

 
{

 
RCC_DeInit(); //将外设 RCC 寄存器重设为缺省值

 
RCC_HSEConfig(RCC_HSE_ON);//设置外部高速晶振（HSE）

 
if(RCC_WaitForHSEStartUp()==SUCCESS) //等待 HSE 起振

 
{

 
RCC_HCLKConfig(RCC_SYSCLK_Div1);//设置 AHB 时钟（HCLK）

 
RCC_PCLK1Config(RCC_HCLK_Div2);//设置低速 AHB 时钟（PCLK1）

 
RCC_PCLK2Config(RCC_HCLK_Div1);//设置高速 AHB 时钟（PCLK2）

 
RCC_PLLConfig(div,pllm);//设置 PLL 时钟源及倍频系数

 
RCC_PLLCmd(ENABLE); //使能或者失能 PLL

 
while(RCC_GetFlagStatus(RCC_FLAG_PLLRDY)==RESET);//检查指定的RCC标志位设置与否,PLL就绪

 
RCC_SYSCLKConfig(RCC_SYSCLKSource_PLLCLK);// 设 置 系 统 时 钟（SYSCLK）

 
while(RCC_GetSYSCLKSource()!=0x08);//返回用作系统时钟的时钟源,0x08：PLL 作为系统时钟

 
}

 
 }

 
函数具体实现过程在程序中已经注释，大家可以参考注释。在函数中设置倍频因子时，我们给他传递了形参中的变量，这样做的好处是当你调用此函数时，只需要修改传递给函数形参内的值即可修改系统时钟，无需修改函数内部程序。在未修改系统时钟时，系统初始化后的时钟是72M，对应着此函数参数设置如下：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-ebb6e15debb24d8b84b3cca933111d48!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
如果现在我们想让系统时钟为36M，只需要将参数值修改即可，如下：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-900e1d62fe0942ab83b796f5875955f0!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
此时修改的是div这个参数值，此参数用来对HSE时钟分频系数设置，从时钟树可知，HSE可以直接流入到PLLSRC，还可以经过2分频后给PLLSRC。它的取值为RCC_PLLSource_HSE_Div1 或 RCC_PLLSource_HSE_Div2。 最后我们可以通过一个LED指示灯闪烁速度来反映系统时钟修改后的效果。 主函数代码如下：

 
int main()

 
{

 
LED_Init();

 
RCC_HSE_Config(RCC_PLLSource_HSE_Div2,RCC_PLLMul_9);//36M

 
while(1)

 
{

 
 GPIO_ResetBits(LED_PORT,GPIO_Pin_1);//点亮 D1

 
 ms(1000000);

 
 GPIO_SetBits(LED_PORT,GPIO_Pin_1);

 
 ms(1000000);

 
}

 
}

 
课后作业

 
（1）通过修改系统时钟调节LED闪烁速度 

 
（2）可以尝试调节系统时钟超过72M，看看效果是什么样（这里仅推荐大家 尝试，不推荐后面使用）