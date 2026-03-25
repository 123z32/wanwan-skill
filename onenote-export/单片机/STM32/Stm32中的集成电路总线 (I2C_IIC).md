# Stm32中的集成电路总线 (I2C/IIC)

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-10T13:11:43Z

Stm32中的集成电路总线 (I2C/IIC)
 
 
 
 
 

 

 
在Stm32中使用I2C有两种方案，一是软件模拟I2C，二是硬件I2C。两种方案各有各的优缺点，因此了解清楚才能选择适合的。

 

 
软件模拟I2C

 
优点：可以用在任何GPIO口；不会发生卡死(最多出错)

 
硬件I2C

 
优点：速度比软件模拟快；容易出现卡死的问题

 
关于硬件I2C卡死问题具体可以看

 

 
卡死原因分析：浅谈STM32硬件I2C[浅谈STM32硬件I2C的 - 纪客老白 (jikelaobai.com)

 
具体测试结论：STM32 硬件I2C 到底是不是个坑？[STM32 硬件I2C 到底是不是个坑？ - Ady Lee - 博客园 (cnblogs.com)

 
总结一下Stm32的硬件I2C问题：

 
1.当时钟频率太高时容易出问题，出问题的概率和时钟频率成正比。

 
2.当存在中断会打断硬件IIC工作时(中断会导致)，容易出现问题。

 

 
硬件I2C的发送流程图：

 ![Stm32_I2C_主机发送](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-17a0f07fd39f4feb8b102fc9245fa35a!1-9E53C6D99C1E5AD1!270/$value)
 

 
硬件I2C的接收流程图：

 ![Stm32_I2C_主机接收](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-b0f36422e2104053933d6cc5f7cc0935!1-9E53C6D99C1E5AD1!270/$value)
 

 

 

 
/*

 
Stm32 使用 硬件I2C 作为主机发送/接收 示例代码

 
*/

 

 
#define OLED_ADDRESS 0x78 //定义一个OLED模块的从机地址

 

 
void I2C_Config(void)

 
{

 
//使能I2C与GPIO时钟

 
RCC_APB1PeriphClockCmd (RCC_APB1ENR_I2C1EN, ENABLE);

 
 RCC_APB2PeriphClockCmd (RCC_APB2Periph_GPIOB, ENABLE);

 

 
//初始化GPIO，配置PB6与PB7为复用开漏输出

 
GPIO_InitTypeDef GPIO_InitStructure;

 
 GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_OD;

 
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;

 
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6 | GPIO_Pin_7;

 
 GPIO_Init (GPIOB, &GPIO_InitStructure);

 

 
//开始初始化I2C

 
I2C_InitTypeDef I2C_InitStructure;

 

 
//使用I2C模式，因为Stm32的I2C硬件外设支持扩展SMBus协议，因此要指定I2C模式

 
I2C_InitStructure.I2C_Mode = I2C_Mode_I2C;

 

 
I2C_InitStructure.I2C_AcknowledgedAddress = I2C_AcknowledgedAddress_7bit; //七位从机地址

 
I2C_InitStructure.I2C_OwnAddress1 = 0x11; //自己作为从机时的地址

 
I2C_InitStructure.I2C_Ack = I2C_Ack_Enable; //默认发送应答

 

 
//配置时钟线(SCL)占空比为低高电平之比为2，仅在I2C的高速模式(100~400 kHz)下有效，标准模式下为1:1

 
//原因是SCL低电平时需要变化SDA电平，因此需要更多时间 

 
I2C_InitStructure.I2C_DutyCycle = I2C_DutyCycle_2;

 

 
//时钟频率，单位Hz，400000 => 400kHz

 
I2C_InitStructure.I2C_ClockSpeed = 400000;

 

 
I2C_Init (I2C1, &I2C_InitStructure);

 
I2C_Cmd (I2C1, ENABLE);

 

 
}

 

 
//封装一个函数用于等待标准事件，包含超时返回，避免卡死

 
void I2C_WaitEvent(I2C_TypeDef* I2Cx, uint32_t I2C_EVENT)

 
{

 
uint16_t t = 10000;

 
while(!I2C_CheckEvent(I2Cx, I2C_EVENT) && t-->0);

 
}

 

 
//指定地址写

 
void I2C_WriteReg(uint8_t RegAddr, uint8_t Data)

 
{

 
//等待总线不繁忙

 
while(I2C_GetFlagStatus(I2C1, I2C_FLAG_BUSY));

 

 
//生成一个起始信号

 
I2C_GenerateSTART (I2C1,ENABLE);

 
I2C_WaitEvent (I2C1, I2C_EVENT_MASTER_MODE_SELECT); //等待EV5

 

 
//发送七位从机地址(OLED_ADDRESS)进行寻找从机。I2C_Direction_Transmitter表示写，会自动设置最低位为1

 
I2C_Send7bitAddress (I2C1, OLED_ADDRESS, I2C_Direction_Transmitter);

 
I2C_WaitEvent (I2C1, I2C_EVENT_MASTER_TRANSMITTER_MODE_SELECTED); //等待EV6

 

 
//发送一个字节(寄存器地址)

 
I2C_SendData (I2C1, RegAddr);

 
I2C_WaitEvent (I2C1, I2C_EVENT_MASTER_BYTE_TRANSMITTING); //等待EV8

 

 
//发送一个字节(数据)

 
I2C_SendData(I2C1, Data);

 
I2C_WaitEvent (I2C1, I2C_EVENT_MASTER_BYTE_TRANSMITTED); //等待EV8_2

 

 
//生成停止信号

 
I2C_GenerateSTOP(I2C1, ENABLE);

 
}

 

 
//指定地址读

 
uint8_t I2C_ReadReg(uint8_t RegAddress)

 
{

 
uint8_t Data;

 

 
 //等待总线不繁忙

 
while(I2C_GetFlagStatus(I2C1, I2C_FLAG_BUSY));

 
 

 
 //生成一个起始信号

 
I2C_GenerateSTART(I2C2, ENABLE);

 
MPU6050_WaitEvent(I2C2, I2C_EVENT_MASTER_MODE_SELECT); //等待EV5

 

 
 //发送七位从机地址(OLED_ADDRESS)进行寻找从机。I2C_Direction_Transmitter表示写，会自动设置最低位为1

 
I2C_Send7bitAddress(I2C2, OLED_ADDRESS, I2C_Direction_Transmitter);

 
I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_TRANSMITTER_MODE_SELECTED);

 
 

 
//发送一个字节(寄存器地址)

 
I2C_SendData(I2C2, RegAddress);

 
I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_BYTE_TRANSMITTED); //等待EV8_2

 

 
 //再次生成起始信号

 
I2C_GenerateSTART(I2C2, ENABLE);

 
I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_MODE_SELECT); //等待EV5

 

 
 //发送七位从机地址(OLED_ADDRESS)进行寻找从机。I2C_Direction_Receiver表示读，会自动设置最低位为0

 
I2C_Send7bitAddress(I2C2, OLED_ADDRESS, I2C_Direction_Receiver);

 
I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_RECEIVER_MODE_SELECTED); //等待EV6

 

 
 //需要在接收之前设置为非应答，因为硬件会在接收完后直接发送 应答/非应答，没有等待时间。

 
I2C_AcknowledgeConfig(I2C2, DISABLE);

 
 //生成停止信号（但是会在当前字节传输或在当前起始条件发出后产生停止条件，因此可以提前给）

 
I2C_GenerateSTOP(I2C2, ENABLE);

 

 
I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_BYTE_RECEIVED); //等待EV7

 
Data = I2C_ReceiveData(I2C2); //读取接收到的数据

 

 
I2C_AcknowledgeConfig(I2C2, ENABLE); //恢复为默认发送应答

 

 
return Data;

 
}