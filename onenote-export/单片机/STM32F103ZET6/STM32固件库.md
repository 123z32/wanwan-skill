# STM32固件库

> 来源: OneNote > 单片机 > STM32F103ZET6
> 修改: 2025-02-03T08:43:35Z

STM32固件库
 
 
 
 
 

 
CMSIS标准

 
什么是CMSIS标准？CMSIS标准英文全称是Cortex MicroController Software Interface Standard，翻译为中文意思就是ARM Cortex微控制器软件接口标准。由于基于Cortex核的芯片厂商很多，不只是ST公司，为了解决不同 厂家的Cortex核芯片软件兼容的问题，ARM和这些厂家就建立了这套CMSIS标准。

 
 我们可以通过一个基于CMSIS标准的应用程序框图来看其重要性。如图 8.1.1 所示：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-e879b88f4dfa4cfcab143e1f2f8a9fb6!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
从图8.1.1可以看出，CMSIS处于中间层，向上提供给用户程序和实时操作 系统所需的函数接口，向下负责与内核和其他外设通信。假如没有CMSIS标准， 基于Cortex的芯片厂商就会设计出自己喜欢的风格库函数。因此CMSIS标准就是要强制他们必须按照这个标准来设计。

 
 在CMSIS 框架内又分为3个基本功能层：

 
（1）核内外设访问层：ARM 公司提供的访问，定义处理器内部寄存器地址以及功能函数。 -

 
（2）中间件访问层：定义访问中间件的通用API，由ARM提供，芯片厂商 根据需要更新。

 
（3）外设访问层：定义硬件寄存器的地址以及外设的访问函数，比如ST公司提供的固件库外设驱动文件（stm32f10x_gpio.c等文件）就是在这个访问层。

 

 
 总的来说其实CMSIS就是统一各芯片厂商固件库内函数的名称，比如在系统初始化的时候使用的是SystemInit这个函数名，那么CMSIS标准就是强制所有使用Cortex核设计芯片的厂商内固件库系统初始化函数必须为这个名字，不能修改。又比如对GPIO口输出操作的函数：GPIO_SetBits，此函数名也是不能随便定义的。更多关于CMSIS标准介绍，大家可以百度搜索下，这里就不多解释。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-64ed46a964cd4676bf17b76b936d6031!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-1add0ffa3e2c4ccdb970a7c026f8a5bf!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 

 
文件

 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-f45e616740c54f0ea26e4309473c0e13!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
core_cm3.h 文件位于“\STM32最新固件库 v3.5\Libraries\CMSIS\CM3\CoreSupport”目录下，说明此文件属于 CMSIS 标准文件，是用来提供进入M3内核的接口文件，属于CMSIS的核心文件，由ARM提供。对于所有M3内核的芯片来说这个文件都是相同的，不需要我们修改。

 
 stm32f10x.h 、system_stm32f10x.h 和 system_stm32f10x.c 文件存放在 “\STM32 最新固件库 v3.5\Libraries\CMSIS\CM3\DeviceSupport\ST\STM32F10x”目录下， system_stm32f10x.h 是片上外设接入层系统头文件。主要是申明设置系统及总线时钟相关的函数。与其对应的源文件是system_stm32f10x.c。这个文件里面有一个非常重要的 SystemInit()函数申明，这个函数在我们系统启动的时候都会调用，用来设置系统的整个系统和总线时钟。而stm32f10x.h是STM32F10x的头文件，类似于51单片机的reg.51，在开发STM32F10x程序的时候基本上都会调用这个头文件，可见其重要性。此文件内部封装了STM32的总线、内存和外设寄存器等，同时该文件还包含了一些时钟相关的定义和中断相关定义等。

 
stm32f10x_ppp.c文件是STM32 外设的驱动源文件，比如stm32f10x_gpio.c 文件。里面已经封装好操作GPIO外设底层的内容，提供给我们使用的是一些API函数。stm32f10x_ppp.h 就是对应的头文件。还有stm32f10x_rcc.c、misc.c和 v3.5\Libraries\STM32F10x_StdPeriph_Driver”内。 stm32f10x_it.c 文件用于存放中断函数，不过中断函数也可以放在其他工程文件内，所以这个文件很少操作，对应的stm32f10x_it.h文件是它的头文件。 stm32f10x_conf.h文件是配置文件，用于删减我们使用的外设头文件，比如使用GPIO外设，那么就需要调用stm32f10x_gpio.h头文件，如果不使用GPIO外设，可以将此头文件注释掉，一般情况下我们不会对这个配置文件操作，因为如果不使用一个外设，可以在工程内不调用即可。这几个文件存放在“\STM32最新固件库v3.5\Project\STM32F10x_StdPeriph_Template”内。 Application.c 文件用于存放用户编写的应用程序，文件名可以根据个人爱好命名。我们通常会命名为main.c，表示存放我们的主函数代码。 在后面我们创建工程模板时，添加这些文件还不够，还要将STM32的启动文件添加进来，否则系统不能启动。ST固件库提供的启动文件有很多，需根据使 用的STM32芯片来选择，因为开发板上使用的是高容量的STM32F1芯片，所以选 择startup_stm32f10x_hd.s。启动文件 startup_stm32f10x_hd.s 存放在 “\STM32 最新固件库 v3.5\Libraries\CMSIS\CM3\DeviceSupport\ST\STM32F10x\startup\arm”内。

 

 
库帮助文档使用

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-fc6af88acd374cf896d321750156cf9e!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-2d81ff275688492db92aa1ce5bb11e74!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
要查找哪个外设的库函数，只需要找到对应的外设名称即可。比如要查找对 GPIO 外设操作的库函数，我们可以在这个列表下往下拉找到GPIO栏，其中 Functions 列表下就是GPIO所有操作的库函数如图8.3.3所示：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-53c84e05c48f40ca8d7f99704b36cab8!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
假如我们先在要查找GPIO_Init函数的功能说明及使用方法，可以在下拉列 表中点击这个函数名即可进入。在函数介绍内就有函数的原形、功能简介、参数说明、函数返回值等信息。如图8.3.4所示：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-e8c6372885af4518bec6a4147f0ee6a3!1-9E53C6D99C1E5AD1!s8ac699eba1fc464baa8c0ee92e0ce9e2/$value)
 
这里给大家介绍的是使用库函数帮助文档来查找函数功能说明等信息，还可 以通过固件库源码来查找，其实库函数帮助文档就是从固件库源码转换过而来。通过固件库查找在后面创建工程模板的时候会给大家介绍，非常简单，如果对英文感冒的朋友，还可以参考《STM32固件库使用手册(中文翻译版)》文档，该文档是上面固件库的中文翻译版，只不过有些函数没有，还有些地方可能与实际固 件库函数有点差别，不过大部分还是一样的，完全可以借鉴，后面在编写程序的过程中，我们就会经常使用到它.