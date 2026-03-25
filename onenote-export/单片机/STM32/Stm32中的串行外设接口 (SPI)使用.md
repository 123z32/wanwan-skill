# Stm32中的串行外设接口 (SPI)使用

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-10T13:15:18Z

Stm32中的串行外设接口 (SPI)使用
 
 
 
 
 

 

 
/*

 
SPI使用的示例例子

 
*/

 
void SPI2_Init(void)

 
{

 
//使能时钟

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE );

 
RCC_APB1PeriphClockCmd(RCC_APB1Periph_SPI2, ENABLE );

 
 

 
//初始化GPIO，配置PB13、PB14、PB15为复用推挽输出

 
 GPIO_InitTypeDef GPIO_InitStructure;

 
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_13 | GPIO_Pin_14 | GPIO_Pin_15;

 
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;

 
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;

 
GPIO_Init(GPIOB, &GPIO_InitStructure);

 

 
 GPIO_SetBits(GPIOB,GPIO_Pin_13|GPIO_Pin_14|GPIO_Pin_15); //配置PB13、PB14、PB15为上拉

 

 
//开始 初始化SPI

 
SPI_InitTypeDef SPI_InitStructure;

 

 
//设置SPI单向或者双向的数据模式:SPI设置为双线双向全双工

 
SPI_InitStructure.SPI_Direction = SPI_Direction_2Lines_FullDuplex;

 

 
//设置SPI工作模式:设置为主SPI

 
SPI_InitStructure.SPI_Mode = SPI_Mode_Master;

 

 
//设置SPI的数据大小:SPI发送接收8位帧结构

 
SPI_InitStructure.SPI_DataSize = SPI_DataSize_8b;

 

 
//串行同步时钟的空闲状态为高电平

 
SPI_InitStructure.SPI_CPOL = SPI_CPOL_High;

 

 
//串行同步时钟的第二个跳变沿数据被采样

 
SPI_InitStructure.SPI_CPHA = SPI_CPHA_2Edge;

 

 
//NSS信号由硬件（NSS管脚）还是软件（使用SSI位）管理:内部NSS信号有SSI位控制

 
SPI_InitStructure.SPI_NSS = SPI_NSS_Soft;

 

 
//设置波特率预分频的值:波特率预分频值为256

 
SPI_InitStructure.SPI_BaudRatePrescaler = SPI_BaudRatePrescaler_256;

 

 
//指定数据传输从MSB位还是LSB位开始:数据传输从MSB位开始

 
SPI_InitStructure.SPI_FirstBit = SPI_FirstBit_MSB;

 

 
//CRC值计算的多项式

 
SPI_InitStructure.SPI_CRCPolynomial = 7;

 

 
SPI_Init(SPI2, &SPI_InitStructure); 

 
SPI_Cmd(SPI2, ENABLE); //使能SPI外设

 

 
SPI2_ReadWriteByte(0xFF); 

 
} 

 

 
//设置 SPI 的波特率预分频值

 
void SPI2_SetSpeed(u8 BaudRatePrescaler)

 
{

 
assert_param(IS_SPI_BAUDRATE_PRESCALER(BaudRatePrescaler));

 
SPI2->CR1 &= 0XFFC7; //清零位5:3 

 
SPI2->CR1 |= BaudRatePrescaler; //设置SPI2速度 

 
SPI_Cmd(SPI2, ENABLE);

 
} 

 

 
//发送一个数据并收回一个数据

 
u8 SPI2_ReadWriteByte(u8 TxData)

 
{ 

 
u8 retry = 0;

 
//检查指定的SPI标志位设置与否:发送缓存空标志位

 
while (SPI_I2S_GetFlagStatus(SPI2, SPI_I2S_FLAG_TXE) == RESET) {

 
retry++;

 
if(retry>200)return 0;

 
}

 
SPI_I2S_SendData(SPI2, TxData); //通过外设SPIx发送一个数据

 

 
retry = 0;

 
//检查指定的SPI标志位设置与否:接受缓存非空标志位

 
while (SPI_I2S_GetFlagStatus(SPI2, SPI_I2S_FLAG_RXNE) == RESET){

 
retry++;

 
if(retry>200)return 0;

 
}

 
return SPI_I2S_ReceiveData(SPI2); //返回通过SPIx最近接收的数据 

 
}