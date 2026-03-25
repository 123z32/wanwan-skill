# Stm32中的直接存储器存取 (DMA)

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-10T13:00:45Z

Stm32中的直接存储器存取 (DMA)
 
 
 
 
 

 ![DMA基础结构_江科大](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-928c16328c37409faba5b9fda1f6139b!1-9E53C6D99C1E5AD1!270/$value)
 

 
DMA 全程 Direct Memory Access (直接存储器存取)，功能就是数据复制，优点就是能代替CPU负责数据复制，让CPU空出来处理其他任务。

 
另外，根据查资料得到，DMA的搬运速度没有CPU搬运的速度快的。详细可以看这里

 

 

 

 
数据复制方向支持：存储器到存储器、存储器到外设、外设到存储器。其中因为Flash一般为只读，所以存储器到存储器为 Flash到SRAM 、SRAM到SRAM。

 

 
数据宽度：

 
支持 字节(Byte，8位)、半字(HalfWord，16位)、字(Word，32位)，支持不同宽度的数据复制，复制对齐为低位对齐。例如：半字(0x1122)复制到字节，则会把低八位复制过去，结果为0x22；半字(0x1122)复制字，则会把半字复制到字的低位，结果为0x00001122。

 

 
地址自增：

 

 

 

 
模式：正常模式(复制完就停下)、循环模式(复制完重新开始，循环模式不可用于存储器到存储器)

 

 
DMA1的请求对应通道：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-faedded6eb8649a59facb57e80ad8a8a!1-9E53C6D99C1E5AD1!270/$value)
 
DMA2的请求对应通道：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-a5f7f98a019a4065a98b1fae0c57d664!1-9E53C6D99C1E5AD1!270/$value)
 
中断与标志位：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-976775a66edd4002ab40e9a06bf3d5c7!1-9E53C6D99C1E5AD1!270/$value)
 
DMAy_FLAG_GLx：全局标志，一次性控制三个标志位。

 

 

 

 
/*

 
DMA 内存到内存 例子

 
*/

 
uint16_t MyDMA_Size; //用于二次开始的时候重置复制次数

 

 
void MyDMA_Init(uint32_t AddrA, uint32_t AddrB, uint16_t Size)//配置DMA

 
{

 
 RCC_AHBPeriphClockCmd(RCC_AHBPeriph_DMA1, ENABLE); //使能DMA1的时钟

 
 

 
MyDMA_Size = Size; //记录一下，开始复制的时候要设置

 

 
DMA_InitTypeDef DMA_InitStructure;

 
DMA_InitStructure.DMA_PeripheralBaseAddr = AddrA; //外设基地址，当用存储器到存储器时，可写存储器地址

 
DMA_InitStructure.DMA_PeripheralDataSize = DMA_PeripheralDataSize_Byte; //外设数据宽度

 
DMA_InitStructure.DMA_PeripheralInc = DMA_PeripheralInc_Enable; //外设地址自增

 
DMA_InitStructure.DMA_MemoryBaseAddr = AddrB; //存储器基地址

 
DMA_InitStructure.DMA_MemoryDataSize = DMA_MemoryDataSize_Byte; //存储器数据宽度

 
DMA_InitStructure.DMA_MemoryInc = DMA_MemoryInc_Enable; //存储器地址自增

 
DMA_InitStructure.DMA_DIR = DMA_DIR_PeripheralSRC; //数据传输方向：SRC外设为源地址，DST外设为目标地址

 
DMA_InitStructure.DMA_BufferSize = Size; //需要复制次数，总复制长度=数据宽度*复制次数

 
DMA_InitStructure.DMA_Mode = DMA_Mode_Normal; //模式：Normal正常模式，Circular循环模式

 
DMA_InitStructure.DMA_M2M = DMA_M2M_Enable; //是否为存储器到存储器(如果是则只能软件触发开始)

 
DMA_InitStructure.DMA_Priority = DMA_Priority_Medium; //优先级:z'ji

 
DMA_Init(DMA1_Channel1, &DMA_InitStructure); //配置DMA1的通道1，这里因为是存储器到存储器，所以通道可以随便选

 

 
 //因为还没有给DMA使能，因此没有开始转换

 
}

 

 
void MyDMA_Transfer(void)//DMA使能

 
{

 
DMA_Cmd(DMA1_Channel1, DISABLE); //赋值复制次数之前要失能DMA

 
DMA_SetCurrDataCounter(DMA1_Channel1, MyDMA_Size); //赋值复制次数

 
DMA_Cmd(DMA1_Channel1, ENABLE); //使能DMA，开始转换

 

 
while (DMA_GetFlagStatus(DMA1_FLAG_TC1) == RESET); //等待复制完成

 
DMA_ClearFlag(DMA1_FLAG_TC1); //清除标志位

 
}

 

 

 

 

 

 

 
/*

 
DMA 外设到存储器 例子

 
ADC多通道

 
*/

 

 
uint16_t AD_Value[4]; //用于保存ADC转换完成的结果

 

 
void AD_Init(void)

 
{

 
 //使能时钟

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1, ENABLE);

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

 
RCC_AHBPeriphClockCmd(RCC_AHBPeriph_DMA1, ENABLE);

 

 
 //配置ADC时钟频率为APB2时钟的6分频

 
RCC_ADCCLKConfig(RCC_PCLK2_Div6);

 

 
 //配置4个IO口

 
GPIO_InitTypeDef GPIO_InitStructure;

 
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AIN;

 
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1 | GPIO_Pin_2 | GPIO_Pin_3;

 
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;

 
GPIO_Init(GPIOA, &GPIO_InitStructure);

 

 
 //配置规则组

 
ADC_RegularChannelConfig(ADC1, ADC_Channel_0, 1, ADC_SampleTime_55Cycles5);

 
ADC_RegularChannelConfig(ADC1, ADC_Channel_1, 2, ADC_SampleTime_55Cycles5);

 
ADC_RegularChannelConfig(ADC1, ADC_Channel_2, 3, ADC_SampleTime_55Cycles5);

 
ADC_RegularChannelConfig(ADC1, ADC_Channel_3, 4, ADC_SampleTime_55Cycles5);

 

 
 //初始化ADC为连续扫描模式

 
ADC_InitTypeDef ADC_InitStructure;

 
ADC_InitStructure.ADC_Mode = ADC_Mode_Independent;

 
ADC_InitStructure.ADC_DataAlign = ADC_DataAlign_Right;

 
ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None;

 
ADC_InitStructure.ADC_ContinuousConvMode = ENABLE;

 
ADC_InitStructure.ADC_ScanConvMode = ENABLE;

 
ADC_InitStructure.ADC_NbrOfChannel = 4;

 
ADC_Init(ADC1, &ADC_InitStructure);

 

 
 //具体看上面存储器到存储器例子

 
DMA_InitTypeDef DMA_InitStructure;

 
DMA_InitStructure.DMA_PeripheralBaseAddr = (uint32_t)&ADC1->DR; //外设基地址为ADC1的DR寄存器

 
DMA_InitStructure.DMA_PeripheralDataSize = DMA_PeripheralDataSize_HalfWord;

 
DMA_InitStructure.DMA_PeripheralInc = DMA_PeripheralInc_Disable;

 
DMA_InitStructure.DMA_MemoryBaseAddr = (uint32_t)AD_Value;

 
DMA_InitStructure.DMA_MemoryDataSize = DMA_MemoryDataSize_HalfWord;

 
DMA_InitStructure.DMA_MemoryInc = DMA_MemoryInc_Enable;

 
DMA_InitStructure.DMA_DIR = DMA_DIR_PeripheralSRC;

 
DMA_InitStructure.DMA_BufferSize = 4;

 
DMA_InitStructure.DMA_Mode = DMA_Mode_Circular; //循环模式

 
DMA_InitStructure.DMA_M2M = DMA_M2M_Disable;

 
DMA_InitStructure.DMA_Priority = DMA_Priority_Medium;

 
DMA_Init(DMA1_Channel1, &DMA_InitStructure);

 

 
DMA_Cmd(DMA1_Channel1, ENABLE); //使能时钟，因为非存储器到存储器，所以要硬件请求才能触发开始复制

 
ADC_DMACmd(ADC1, ENABLE); //允许ADC1可以提交请求触发DMA的数据复制

 
ADC_Cmd(ADC1, ENABLE); //使能ADC

 

 
 //ADC校准

 
ADC_ResetCalibration(ADC1);

 
while (ADC_GetResetCalibrationStatus(ADC1) == SET);

 
ADC_StartCalibration(ADC1);

 
while (ADC_GetCalibrationStatus(ADC1) == SET);

 

 
 //软件触发开始转换

 
ADC_SoftwareStartConvCmd(ADC1, ENABLE); 

 
//因为ADC为连续扫描模式、DMA为循环模式，所以只需要触发开始转换后，硬件就会不断得转换并把数据复制到AD_Value 数组

 
}