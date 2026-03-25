# Stm32中的控制器局域网 (bxCAN)使用

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-10T13:28:18Z

Stm32中的控制器局域网 (bxCAN)使用
 
 
 
 
 

 

 
Stm32中的CAN架构：

 

 
设置

 

 
 
- 速率：CAN总线的速率常用的都是125k到500k（一般使用500k），尽管它的最大速率是1Mbps。但明显的是，最大值往往要求环境更加高，导致容易出现问题。
 
- 工作模式：初始化模式、正常模式、睡眠模式
 
- 测试模式：静默模式、回环模式、回环静默模式
 
- 调试模式：当MCU处于调试模式时，Cortex-M3核心处于暂停状态，提供配置，可以使bxCAN继续正常工作或停止工作（CAN是异步通讯，因此需要这个）
 

 
发送：

 

 
 
- 3个发送邮箱：可以配置发送优先级(按写入先后 / 按标识符数值)
 
- 自动重传：发送失败则自动重新发送，直至成功
 

 

 
接收：

 

 
 
- 2个三级深度接收邮箱(FIFO)：共可以接收6个报文
 
- 注：FIFO是英文First In First Out 的缩写，是一种先进先出的数据缓存器
 
- 锁定模式：锁定状态下，接收溢出则丢弃；非锁定状态下，接收溢出则覆盖
 

 

 
过滤器：

 

 
 
- 
14个位宽可配置的标识符过滤器组

 
 
- 一个位宽可配置为1个32位掩码模式/2个32位标识符列表模式/2个16位掩码模式/4个16位标识符列表模式
 

 
 
- 
过滤模式

 
 
- 标识符列表模式：丢弃掉非指定标识符的报文
 
- 掩码模式：可以指定标识符某些位是非必要的后进行比对
 

 
 

 
测试模式图解：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-31187991137343b29d49761bb451571f!1-9E53C6D99C1E5AD1!270/$value)
 

 

 
过滤器：

 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-978078bbd9b347e2ba0e6bd77d9452e6!1-9E53C6D99C1E5AD1!270/$value)
 

 
CAN_Mode_Init()

 
{

 
//使能时钟

 
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

 
RCC_APB1PeriphClockCmd(RCC_APB1Periph_CAN1, ENABLE);

 

 
//初始化CAN_RX为上拉输入

 
GPIO_InitTypeDef GPIO_InitStructure;

 
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_11;

 
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;

 
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;

 
GPIO_Init(GPIOA, &GPIO_InitStructure);

 

 
//初始化CAN_TX为复用推挽输出

 
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12;

 
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP; 

 
GPIO_Init(GPIOA, &GPIO_InitStructure);

 

 
// CAN单元设置

 
CAN_InitTypeDef CAN_InitStructure;

 
CAN_InitStructure.CAN_TTCM = DISABLE; //非时间触发通信模式

 
CAN_InitStructure.CAN_ABOM = DISABLE; //软件自动离线管理

 
CAN_InitStructure.CAN_AWUM = DISABLE; //睡眠模式通过软件唤醒(清除CAN->MCR的SLEEP位)

 
CAN_InitStructure.CAN_NART = ENABLE; //禁止报文自动传送

 
CAN_InitStructure.CAN_RFLM = DISABLE; //报文不锁定,新的覆盖旧的

 
CAN_InitStructure.CAN_TXFP = DISABLE; //优先级由报文标识符决定

 
CAN_InitStructure.CAN_Mode = CAN_Mode_LoopBack; //模式设置： mode:0,普通模式;1,回环模式;

 
// 设置波特率 500kMps

 
CAN_InitStructure.CAN_Prescaler = 4; //预分频系数

 
CAN_InitStructure.CAN_SJW = CAN_SJW_1tq; //重新同步跳跃宽度 CAN_SJW_1tq ~ CAN_SJW_4tq

 
CAN_InitStructure.CAN_BS1 = CAN_BS1_9tq; //CAN_BS1_1tq ~CAN_BS1_16tq

 
CAN_InitStructure.CAN_BS2 = CAN_BS2_8tq; //CAN_BS2_1tq ~ CAN_BS2_8tq

 
CAN_Init(CAN1, &CAN_InitStructure);

 

 
CAN_FilterInitTypeDef CAN_FilterInitStructure;

 
CAN_FilterInitStructure.CAN_FilterNumber = 0; //过滤器0，可以为0~13

 
CAN_FilterInitStructure.CAN_FilterMode = CAN_FilterMode_IdMask; //掩码模式

 
CAN_FilterInitStructure.CAN_FilterScale = CAN_FilterScale_32bit; //32位

 
CAN_FilterInitStructure.CAN_FilterIdHigh = 0x0000; //32位标识符

 
CAN_FilterInitStructure.CAN_FilterIdLow = 0x0000; 

 
CAN_FilterInitStructure.CAN_FilterMaskIdHigh = 0x0000; //32位掩码，1:要求一致，0:不限制

 
CAN_FilterInitStructure.CAN_FilterMaskIdLow = 0x0000;

 
CAN_FilterInitStructure.CAN_FilterFIFOAssignment = CAN_Filter_FIFO0; // 关联到FIFO0

 
CAN_FilterInitStructure.CAN_FilterActivation = ENABLE; // 使能过滤器0

 
CAN_FilterInit(&CAN_FilterInitStructure); // 滤波器初始化

 

 

 
/* 

 
用于开启中断

 

 
CAN_ITConfig(CAN1, CAN_IT_FMP0, ENABLE); // FIFO0消息挂号中断允许

 

 
NVIC_InitTypeDef NVIC_InitStructure;

 
NVIC_InitStructure.NVIC_IRQChannel = USB_LP_CAN1_RX0_IRQn;

 
NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1; // 主优先级为1

 
NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0; // 次优先级为0

 
NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;

 
NVIC_Init(&NVIC_InitStructure);

 
*/

 
}

 

 
//中断函数模板

 
void USB_LP_CAN1_RX0_IRQHandler(void)

 
{

 
CanRxMsg RxMessage;

 
int i = 0;

 
CAN_Receive(CAN1, 0, &RxMessage);

 
for (i = 0; i < 8; i++)

 
printf("rxbuf[%d]:%d\r\n", i, RxMessage.Data[i]);

 
}

 

 
//发送报文，返回0为成功，否则失败

 
u8 Can_Send_Msg(u8 *msg, u8 len)

 
{

 
u8 mbox;

 
u16 i = 0;

 
CanTxMsg TxMessage;

 
TxMessage.StdId = 0x12; //标准标识符

 
TxMessage.ExtId = 0x12; //设置扩展标示符

 
TxMessage.IDE = CAN_Id_Standard; //表明为标准帧

 
TxMessage.RTR = CAN_RTR_Data; //表明为数据帧

 
TxMessage.DLC = len; //要发送的数据长度

 
for (i = 0; i < len; i++) //复制数据到结构体

 
TxMessage.Data[i] = msg[i];

 
mbox = CAN_Transmit(CAN1, &TxMessage); //填入发送邮箱，mbox为被填入的邮箱号

 
i = 0;

 
while ((CAN_TransmitStatus(CAN1, mbox) == CAN_TxStatus_Failed) && (i < 0XFFF))

 
i++; //等待发送结束

 
if (i == 0XFFF)

 
return 1; //超时

 
return 0;

 
}

 

 
//接收数据查询，成功返回数据长度，没有返回0

 
u8 Can_Receive_Msg(u8 *buf)

 
{

 
u32 i;

 
CanRxMsg RxMessage;

 
if (CAN_MessagePending(CAN1, CAN_FIFO0) == 0) //查询邮箱有多少条数据

 
return 0;

 
CAN_Receive(CAN1, CAN_FIFO0, &RxMessage); //读取数据

 
for (i = 0; i < 8; i++)

 
buf[i] = RxMessage.Data[i];

 
return RxMessage.DLC;

 
}