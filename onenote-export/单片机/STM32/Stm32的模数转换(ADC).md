# Stm32的模数转换(ADC)

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-10T12:37:59Z

Stm32的模数转换(ADC)
 
 
 
 
 

 
规则组：用于常规使用

 
注入组：用于突发情况使用ADC功能

 

 
规则组和注入组的关系有点类似主线程和中断的关系，若触发开始转换注入组可以 对 正在转换的规则组进行插队。

 

 
输入通道：

 

 
因为Stm32有双ADC模式(两个ADC配合工作)，因此ADC1和ADC2的通道对应的IO基本一样，除了ADC1多出来的温度传感器与内部参考电压通道。

 
 

 | 通道
 | ADC1
 | ADC2
 | ADC3
 
 

 | 通道0
 | PA0
 | PA0
 | PA0
 
 

 | 通道1
 | PA1
 | PA1
 | PA1
 
 

 | 通道2
 | PA2
 | PA2
 | PA2
 
 

 | 通道3
 | PA3
 | PA3
 | PA3
 
 

 | 通道4
 | PA4
 | PA4
 | PA4
 
 

 | 通道5
 | PA5
 | PA5
 | PA5
 
 

 | 通道6
 | PA6
 | PA6
 | PA6
 
 

 | 通道7
 | PA7
 | PA7
 | PA7
 
 

 | 通道8
 | PB0
 | PB0
 | PB0
 
 

 | 通道9
 | PB1
 | PB1
 | 

 
 
 

 | 通道10
 | PC0
 | PC0
 | PC0
 
 

 | 通道11
 | PC1
 | PC1
 | PC1
 
 

 | 通道12
 | PC2
 | PC2
 | PC2
 
 

 | 通道13
 | PC3
 | PC3
 | PC3
 
 

 | 通道14
 | PC4
 | PC4
 | 

 
 
 

 | 通道15
 | PC5
 | PC5
 | 

 
 
 

 | 通道16
 | 温度传感器
 | 

 
 | 

 
 
 

 | 通道17
 | 内部参考电压
 | 

 
 | 

 
 
 

 

 
ADC配置：

 

 
扫描模式：当开始转换后，会根据ADC通道数量(ADC_InitTypeDef.ADC_NbrOfChannel) 按顺序进行N次转换，全部转换完成后设置 EOC(规则组转换结束) 标志位

 

 
非扫描模式：当开始转换后，仅会对规则组位置一的通道进行1次转换，转换完成设置 EOC 标志位

 

 
单次转换：在开始转换后，仅仅对规则组整组进行一次转换

 
连续转换：在开始转换后，会循环对规则组整组进行转换

 

 
间断模式：在开始转换后，进行 N 次转换后停下，并记录当前位置，当下次开始转换时按顺序下去。

 

 
需要使用 ADC_DiscModeChannelCountConfig 设置 N 的值，并使用 ADC_DiscModeCmd 使能模式。

 
举例： N=3，被转换的通道有 0、1、2、3、6、7、9、10

 
第一次触发：转换的序列为 0、1、2

 
第二次触发：转换的序列为 3、6、7

 
第三次触发：转换的序列为 9、10，并产生EOC事件 (注意这里因为到尾了，所以只转换了两个通道)

 
第四次触发：转换的序列 0、1、2

 

 
总结:

 

 
如果将ADC转换比喻为使用音乐软件听歌的话

 

 
ADC_RegularChannelConfig 就是为歌单增加歌曲并设置歌曲的序列

 
ADC_InitTypeDef.ADC_NbrOfChannel 就是歌单中歌曲的数量

 

 
 
- 扫描模式 就是 播放整个歌单的全部歌曲
 
- 非扫描模式 就是只播放歌单的第一首歌曲
 
- 单次转换 就是只播放一次 歌单中全部歌曲(扫描模式) / 歌单的第一首歌曲(非扫描模式)
 
- 连续转换 就是循环播放 歌单中全部歌曲(扫描模式) / 歌单的第一首歌曲(非扫描模式)
 
- 扫描模式&单次转换 = 歌曲中全部歌曲按顺序全部播放一次
 
- 非扫描模式&单次转换 = 只播放一次歌单的第一首歌曲
 
- 扫描模式&连续转换 = 列表循环
 
- 非扫描模式&连续转换 = 单曲循环1
 
- 间断模式 就是一次听 N 首歌曲，并记下听到第几首了，下次接着听下去，当歌单全部歌曲听完后再回到第一首
 

 

 
校准：

 

 
ADC有一个内置的校准模式，能大幅减少因内部电容器组的变化而造成的准精度误差。因此建议每次上电后都执行一次校准。

 

 
在 Stm32F10xxx参考手册(2009中文版本) 中ADC章节有这样一句话：

 

 
启动校准前，ADC必须处于关电状态(ADON=’0’)超过至少两个ADC时钟周期

 

 
事实上，是ST公司的描写错误，而在官网中找到的 2021 版本中已经被更正为

 

 
原文：Before starting a calibration, the ADC must have been in power-on state (ADON bit = ‘1’) for at least two ADC clock cycles.

 
翻译：在开始校准之前，ADC必须处于通电状态(ADON位=“1”) 至少两个ADC时钟周期。

 

 

 

 

 
void AD_Init(void)

 
{

 
 //使能时钟

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1, ENABLE);

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

 

 
 //配置ADC的时钟周期，RCC_PCLK2_Div6 为高速APB2时钟(PCLK2)的6分频

 
RCC_ADCCLKConfig(RCC_PCLK2_Div6);

 

 
 //配置PA0为输入口，模式为模拟输入(GPIO_Mode_AIN)，该模式是ADC专用

 
GPIO_InitTypeDef GPIO_InitStructure;

 
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AIN;

 
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;

 
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;

 
GPIO_Init(GPIOA, &GPIO_InitStructure);

 

 
 //配置规则组，将通道0放在第一个位置，采样时间为55.5个周期(ADC_SampleTime_55Cycles5)

 
ADC_RegularChannelConfig(ADC1, ADC_Channel_0, 1, ADC_SampleTime_55Cycles5);

 

 
 //初始化ADC1

 
ADC_InitTypeDef ADC_InitStructure;

 
ADC_InitStructure.ADC_Mode = ADC_Mode_Independent; //工作在独立模式

 
ADC_InitStructure.ADC_DataAlign = ADC_DataAlign_Right; //数据右对齐

 
ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None; //外部触发源选择不使用外部触发

 
ADC_InitStructure.ADC_ContinuousConvMode = DISABLE; //是否启用连续模式

 
ADC_InitStructure.ADC_ScanConvMode = DISABLE; //是否启用扫描模式

 
ADC_InitStructure.ADC_NbrOfChannel = 1; //进行ADC的通道数量

 
ADC_Init(ADC1, &ADC_InitStructure);

 

 
 //使能ADC1

 
ADC_Cmd(ADC1, ENABLE);

 

 
 //进行校准

 
ADC_ResetCalibration(ADC1); //将校准复位

 
while (ADC_GetResetCalibrationStatus(ADC1) == SET); //等待校准复位完成

 
ADC_StartCalibration(ADC1); //开始校准

 
while (ADC_GetCalibrationStatus(ADC1) == SET); //等待校准完成

 
}

 

 
uint16_t AD_GetValue(void)

 
{

 
ADC_SoftwareStartConvCmd(ADC1, ENABLE); //软件触发开始转换

 
while (ADC_GetFlagStatus(ADC1, ADC_FLAG_EOC) == RESET); //等待转换完成

 
return ADC_GetConversionValue(ADC1); //返回转换得到的数值(0~4095)

 
}