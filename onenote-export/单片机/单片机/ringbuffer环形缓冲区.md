# ringbuffer环形缓冲区

> 来源: OneNote > 单片机 > 单片机
> 修改: 2025-10-31T14:05:05Z

ringbuffer环形缓冲区
 
 
 
 
 

 
ringbuffer称作环形缓冲区，也称作环形队列（circular queue），是一种用于表示一个固定尺寸、头尾相连的缓冲区的数据结构，适合缓存数据流。

 

 
环形缓冲区的一些使用特点如下：

 

 
 
- 当一个数据元素被读取出后，其余数据元素不需要移动其存储位置；
 

 

 
 
- 适合于事先明确了缓冲区的最大容量的情形。缓冲区的容量（长度）一般固定，可以用一个静态数组来充当缓冲区，无需重复申请内存；
 

 

 
 
- 如果缓冲区的大小需要经常调整，就不适合用环形缓冲区，因为在扩展缓冲区大小时，需要搬移其中的数据，这种场合使用链表更加合适；
 

 

 
 
- 因为缓冲区成头尾相连的环形，写操作可能会覆盖未及时读取的数据，有的场景允许这种情况发生，有的场景又严格限制这种情况发生。选择何种策略和具体应用场景相关。
 

 

 
c

 
#include "ringbuffer_u8.h"

 

 
void ringbuffer_u8_init(ringbuffer_u8_type *rb)

 
{

 
 rb->write_index = 0;

 
 rb->read_index = 0;

 
}

 

 
bool ringbuffer_u8_is_empty(ringbuffer_u8_type *rb)

 
{

 
 if (rb->write_index == rb->read_index)

 
 return true;

 
 else

 
 return false;

 
}

 

 
bool ringbuffer_u8_is_full(ringbuffer_u8_type *rb)

 
{

 
 

 
 if ((rb->write_index - rb->read_index + ringbuffer_u8_length) % ringbuffer_u8_length == (ringbuffer_u8_length - 1)){

 
 return true;

 
 }else {

 
 return false;

 
 }

 
}

 

 

 
void ringbuffer_u8_push_back_byte(ringbuffer_u8_type *rb, uint8_t data)

 
{

 
 if(ringbuffer_u8_is_full(rb))

 
 {

 
 rb->read_index++;

 
 rb->read_index %= ringbuffer_u8_length;

 
 }

 
 

 
 rb->buffer[rb->write_index] = data;

 

 
 rb->write_index++;

 
 rb->write_index %= ringbuffer_u8_length;

 
}

 

 
uint8_t ringbuffer_u8_pop_front_byte(ringbuffer_u8_type *rb)

 
{

 
 uint8_t res;

 
 

 
 if(ringbuffer_u8_is_empty(rb))

 
 {

 
 return 0;

 
 }

 
 

 
 res = rb->buffer[rb->read_index];

 
 rb->read_index++;

 
 rb->read_index %= ringbuffer_u8_length;

 
 

 
 return res;

 
}

 

 
uint8_t ringbuffer_u8_read_front_byte(ringbuffer_u8_type *rb, uint8_t counter) //预取地址不变化

 
{

 
 uint8_t res;

 
 

 
 if(ringbuffer_u8_is_empty(rb)){

 
 return 0;

 
 }

 
 res = rb->buffer[rb->read_index+counter];

 
 

 
 return res;

 
}

 

 
void ringbuffer_u8_clear_byte(ringbuffer_u8_type *rb, uint16_t data) //写地址回到读地址

 
 {

 
 rb->write_index = data;

 
 }

 

 
 

 
uint16_t ringbuffer_u8_read_byte(ringbuffer_u8_type *rb) //写地址回到读地址

 
 {

 
 uint16_t index;

 
 index = rb->write_index;

 
 return index;

 
 }

 

 
 

 
 

 
uint32_t ringbuffer_length(ringbuffer_u8_type *rb)

 
 {

 
 uint32_t res;

 
 

 
 if(ringbuffer_u8_is_empty(rb)){

 
 return 0;

 
 }

 
 

 
 res = (rb->write_index - rb->read_index + ringbuffer_u8_length) % ringbuffer_u8_length;

 
 return res;

 
 }

 

 
h

 
#ifndef SRC_BUFFER_RINGBUFFER_U8_H_

 
#define SRC_BUFFER_RINGBUFFER_U8_H_

 

 
#include <stdint.h>

 
#include <stdbool.h>

 
#include <string.h>

 

 
#define ringbuffer_u8_length (512)

 

 
typedef struct

 
{

 
 uint8_t buffer[ringbuffer_u8_length];

 
 

 
 uint16_t write_index;

 
 uint16_t read_index;

 
}ringbuffer_u8_type;

 

 

 
typedef struct

 
{

 
 uint32_t buffer[ringbuffer_u8_length];

 
 

 
 uint16_t write_index;

 
 uint16_t read_index;

 
}ringbuffer_u32_type;

 

 

 
extern void ringbuffer_u8_init(ringbuffer_u8_type *rb);

 

 
extern bool ringbuffer_u8_is_empty(ringbuffer_u8_type *rb);

 

 
extern bool ringbuffer_u8_is_full(ringbuffer_u8_type *rb);

 

 
extern void ringbuffer_u8_push_back_byte(ringbuffer_u8_type *rb, uint8_t data);

 

 
extern uint8_t ringbuffer_u8_pop_front_byte(ringbuffer_u8_type *rb);

 

 
extern uint32_t ringbuffer_length(ringbuffer_u8_type *rb);

 

 
extern void ringbuffer_u8_clear_byte(ringbuffer_u8_type *rb, uint16_t data);

 

 
extern uint16_t ringbuffer_u8_read_byte(ringbuffer_u8_type *rb);

 

 
extern uint8_t ringbuffer_u8_read_front_byte(ringbuffer_u8_type *rb, uint8_t counter);

 

 
#endif /* SRC_BUFFER_RINGBUFFER_U8_H_ */

 

 

 
移植成功案例（基于STC8H）

 
#include <STC8H.h>

 
#include "intrins.h"

 
typedef unsigned char u8;

 
typedef unsigned int u16;

 
typedef unsigned long u32;

 

 
sbit Led1=P0^0;

 
sbit Led2=P0^1;

 
sbit Led3=P0^2;

 
sbit Led4=P0^3;

 
u8 TX1_Cnt; //U1发送计数

 
u8 RX1_Cnt; //U1接收计数

 
bit B_TX1_Busy; //U1发送忙标志

 
u8 RX1_Buffer[16]; //u1接收缓冲

 
u8 TX2_Cnt; //U2发送计数

 
u8 RX2_Cnt; //U2接收计数

 
bit B_TX2_Busy; //U2发送忙标志

 
u8 RX2_Buffer[16]; //u2接收缓冲

 
void Delay1ms(unsigned char x);//当主时钟频率为12M，1ms延时为基准

 
void init_IO();//初始化IO

 
void init_Uart1();//串口1初始化

 
void init_Uart2();//串口2初始化

 
void Uart1Send(char dat);

 
void Uart2Send(char dat);

 
void Uart1SendStr(char *puts);//发送数据

 
void Uart2SendStr(char *puts);//发送数据

 

 
typedef unsigned char uint8_t;

 
typedef unsigned int uint16_t;

 
typedef unsigned long uint32_t;

 
#define RINGBUFFER_SIZE 64

 

 
typedef struct

 
{

 
 uint8_t buffer[RINGBUFFER_SIZE];

 
 uint16_t write_index;

 
 uint16_t read_index;

 
}ringbuffer_t;

 

 
ringbuffer_t uart_ringbuffer;

 
uint8_t frame_data[64];

 
uint8_t frame_length = 0;

 
uint8_t received_data;

 

 

 
void init_IO()

 

 
{

 

 
 RSTCFG=0x50; //开启RST键进入ISP模式

 
 P0M1 = 0x00; P0M0 = 0x00; //设置P0口为准双向口

 
 P1M1 = 0x00; P1M0 = 0x00; //设置P0口为准双向口

 
 P2M1 = 0x00; P2M0 = 0x00; //设置P1口为准双向口

 
 P3M1 = 0x00; P3M0 = 0x00; //设置P3口为准双向口

 
 P4M1 = 0x00; P4M0 = 0x00; //设置P4口为准双向口

 
 P5M1 = 0x00; P5M0 = 0x00; //设置P5口为准双向口

 
 //P4M1=0xc0;P4M0=0x00;//设置P47和46高阻

 
}

 

 
void init_Uart1()//波特率11.0592

 
{

 
 P_SW1|=0x00;//将串口1的引脚切换至P30、P31

 
 SCON=0x50;//模式1，8位可变

 
 T2L = 0xE8; //设置定时初始值

 
T2H = 0xFF; //设置定时初始值

 
AUXR|=0x04; //开启T1定时器1T工作模式

 
AUXR|=0x10; //开启T1定时器T1R=1

 
AUXR|=0x01; //Uart1使用模式1时，指定T2波特率发生器

 
ES=1;

 
B_TX1_Busy = 0;//忙检测

 
 TX1_Cnt = 0;//发送计数

 
 RX1_Cnt = 0;//接收计数

 
}

 

 
void init_Uart2()//波特率11.0592

 
{

 
S2CON=0x10; //打开允许接收

 
T2L = 0xE8; //设置定时初始值

 
T2H = 0xFF; //设置定时初始值

 
AUXR|=0x04; //开启T2定时器1T工作模式

 
AUXR|=0x10; //开启T2定时器T2R=1

 

 
IE2|=0x01;//开启ES=1

 
P_SW2|=0x00;//串口2脚位切换，将串口2脚位切换到P10、P11

 
B_TX2_Busy = 0;//忙检测

 
TX2_Cnt = 0;//发送计数

 
RX2_Cnt = 0;//接收计数

 

 
}

 

 
void Uart2Send(char dat)//u2发送单字符

 
{

 
while(B_TX2_Busy);

 
B_TX2_Busy=1;

 
S2BUF=dat;

 
}

 
void Uart1Send(char dat)//U1发送单字符

 
{

 
while(B_TX1_Busy);

 
B_TX1_Busy=1;

 
 SBUF=dat;

 
}

 

 
void Delay1ms(unsigned char x) //@12.000MHz

 
{

 

 
 unsigned char i, j;

 
 i = 16;

 
 j = 147;

 
 while(x--)

 
 {

 
 do

 
 {

 
 while (--j);

 
 } while (--i);

 
 }

 
}

 

 
void Uart2SendStr(char *puts)//U2发送字符串

 
{

 
 while(*puts)

 
 {

 
 Uart2Send(*puts++);

 
 }

 
}

 

 
void Uart1SendStr(char *puts)//U1发送字符串

 
{

 
 while(*puts)

 
 {

 
 Uart1Send(*puts++);

 
 }

 
}

 

 
void UART2_isr (void) interrupt 8//Uart2串口中断入口

 
{

 
 Led2=~Led2;

 
 if((S2CON & 1) != 0)

 
 {

 
 S2CON &= ~1; //Clear Rx flag

 
 RX2_Buffer[RX2_Cnt++] = S2BUF;

 
 RX2_Cnt&=0x0f;

 
 SBUF=S2BUF;//发送至串口2

 
 }

 
 if((S2CON & 2) != 0)

 
 {

 
 S2CON &= ~2; //Clear Tx flag

 
 B_TX2_Busy = 0;

 
 }

 
}

 
void UART1_isr (void) interrupt 4//Uart1串口中断入口

 
{

 
 Led2=~Led2;

 
 if((SCON & 1) != 0)

 
 {

 
 SCON &= ~1; //Clear Rx flag RI

 
// RX1_Buffer[RX1_Cnt++] = SBUF;

 
// RX1_Cnt&=0x0f;

 
// S2BUF=SBUF;//发送至串口1

 
received_data = SBUF; 

 
if ((uart_ringbuffer.write_index + 1) % RINGBUFFER_SIZE != uart_ringbuffer.read_index)

 
{

 
 uart_ringbuffer.buffer[uart_ringbuffer.write_index] = received_data;

 
 uart_ringbuffer.write_index = (uart_ringbuffer.write_index + 1) % RINGBUFFER_SIZE;

 
}

 
 }

 
 if((SCON & 2) != 0)

 
 {

 
 SCON &= ~2; //Clear Tx flag TI

 
 B_TX1_Busy = 0;

 
P60=0;

 
 } 

 
}

 

 
void RingBuffer_Init(ringbuffer_t *rb)//初始化

 
{

 
 rb->write_index = 0;

 
 rb->read_index = 0;

 
}

 

 
uint16_t RingBuffer_Length(ringbuffer_t *rb)//返回环形缓冲区当前存储的数据元素数量，无论写入和读取的位置关系如何。

 
{

 
 return (rb->write_index - rb->read_index + RINGBUFFER_SIZE) % RINGBUFFER_SIZE;

 
}

 

 
uint8_t RingBuffer_Pop(ringbuffer_t *rb) //从指定的环形缓冲区 rb 中读取并移除一个字节的数据。

 
{

 
uint8_t data1;

 
 if (rb->read_index != rb->write_index) 

 
{

 
 data1 = rb->buffer[rb->read_index];

 
 rb->read_index = (rb->read_index + 1) % RINGBUFFER_SIZE;

 
 return data1;

 
 }

 
 return 0;

 
}

 

 
void Process_Frame(void) 

 
{

 
 while (RingBuffer_Length(&uart_ringbuffer) >= 4) //环型缓冲区内容>4

 
{ 

 
 uint8_t frame_start = uart_ringbuffer.buffer[uart_ringbuffer.read_index];//读帧头

 
 if (frame_start == 0x5A) 

 
{ 

 
//P60=0;

 
 uint8_t frame_length = uart_ringbuffer.buffer[(uart_ringbuffer.read_index + 1) % RINGBUFFER_SIZE];//读帧长

 
if (RingBuffer_Length(&uart_ringbuffer) >= frame_length) 

 
{ 

 
uint8_t i = 0;

 
P60=0;

 
for (i = 0; i < frame_length; i++) //将帧数据送入处理区

 
{

 
frame_data[i] = RingBuffer_Pop(&uart_ringbuffer);

 
 }

 
 frame_length = 0;

 
 }

 
 } 

 
else 

 
{

 
 RingBuffer_Pop(&uart_ringbuffer);

 
 }

 
 } 

 
}

 
void main()

 
{

 
 P_SW2 |= 0x80; //扩展寄存器XFR访问使能

 
 init_IO();

 
init_Uart1();

 
 init_Uart2();

 
 EA=1;

 
//Uart1SendStr("STC8H TEST!");

 
 Uart2SendStr("STC8H TEST!");

 
P6M0=0X00;

 
P6M1=0X00;

 
RingBuffer_Init(&uart_ringbuffer);

 
P60=1;

 
 while(1)

 
 {

 
 if(P34==0)

 
 {

 
 Delay1ms(1);

 
 if(P34==0)

 
 {

 
//Uart2SendStr("STC8H TEST!");

 
//Uart1SendStr("STC8H TEST!");

 
 unsigned char i=0;

 
 for (i = 0; i < 5; i++) 

 
{

 
Uart1Send(frame_data[i]);

 
while(TI);

 
TI=0;

 
 }

 
 }

 
 }

 
 Process_Frame();

 
 //Uart1Send(frame_data[1]);

 
 }

 
}