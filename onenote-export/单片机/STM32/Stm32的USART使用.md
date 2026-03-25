# Stm32的USART使用

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-09T10:24:26Z

Stm32的USART使用
 
 
 
 
 

 
源程序

 
void Serial_Init(void)

 
{

 
 //使用之前需要先启用外设 USART1,GPIOA

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1, ENABLE);

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

 

 
 //初始化TX引脚 PA9 为复用推挽输出 

 
GPIO_InitTypeDef GPIO_InitStructure;

 
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;

 
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;

 
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;

 
GPIO_Init(GPIOA, &GPIO_InitStructure);

 

 
 //初始化RX引脚 PA10 为上拉输入

 
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;

 
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;

 
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;

 
GPIO_Init(GPIOA, &GPIO_InitStructure);

 

 
 //初始化 USART1 为波特率9600，无硬流控，需要收发，无校验，1位停止位

 
USART_InitTypeDef USART_InitStructure;

 
USART_InitStructure.USART_BaudRate = 9600; //波特率9600

 
USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//无硬流控

 
USART_InitStructure.USART_Mode = USART_Mode_Tx | USART_Mode_Rx; //需要收发

 
USART_InitStructure.USART_Parity = USART_Parity_No; //无校验

 
USART_InitStructure.USART_StopBits = USART_StopBits_1; //1位停止位

 
USART_InitStructure.USART_WordLength = USART_WordLength_8b; //字长 8bit

 
USART_Init(USART1, &USART_InitStructure);

 

 
 //开启RXNE标志位到NVIC的输出

 
USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);

 

 
 //设置优先级分配配置

 
NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);

 

 
 //配置 USART1 的中断

 
NVIC_InitTypeDef NVIC_InitStructure;

 
NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;

 
NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;

 
NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;

 
NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;

 
NVIC_Init(&NVIC_InitStructure);

 

 
 //最后使能 USART1

 
USART_Cmd(USART1, ENABLE);

 
}

 

 
void Serial_SendByte(uint8_t Byte)

 
{

 
USART_SendData(USART1, Byte); //填充数据至 USART1的DR寄存器

 
 

 
 //USART_FLAG_TXE: 发送寄存器为空标志位。对USART_DR的写操作时，将该位清零。

 
while (USART_GetFlagStatus(USART1, USART_FLAG_TXE) == RESET); //等待发送完成

 
}

 

 
//USART1 中断函数

 
void USART1_IRQHandler(void)

 
{

 
if (USART_GetITStatus(USART1, USART_IT_RXNE) == SET)

 
{

 
uint8_t Serial_RxData = USART_ReceiveData(USART1); //读取 USART1 收到的字节

 

 

 
 /*

 
 USART_ClearITPendingBit(USART1, USART_IT_RXNE);

 
 这里可以省略手动清除标志位，因为对USART_DR的读操作可以将该位清零。

 
 */

 
}

 
}