# UART

> 来源: OneNote > 单片机 > IAP152K61S2
> 修改: 2025-06-14T13:47:08Z

UART
 
 
 
 
 

 

 
#include <STC15F2K60S2.H>

 

 
typedef unsigned char BYTE;

 
typedef unsigned int WORD;

 

 
void SendData(BYTE dat);

 
void SendString(char *s);

 
bit busy;

 

 
u8 

 
void Uart1_Init(void) //115200bps@12.000MHz

 
{

 
SCON = 0x50; //8位数据,可变波特率

 
AUXR |= 0x01; //串口1选择定时器2为波特率发生器

 
AUXR |= 0x04; //定时器时钟1T模式

 
T2L = 0xE6; //设置定时初始值

 
T2H = 0xFF; //设置定时初始值

 
AUXR |= 0x10; //定时器2开始计时

 
ES = 1; //使能串口1中断

 
}

 

 
int main()

 
{

 
Uart1_Init();

 
EA=1;

 
SendString("STC15F2K60S2\r\nUart Test !\r\n");

 
while(1);

 
}

 
void Uart1_Isr(void) interrupt 4

 
{

 
if (TI) //检测串口1发送中断

 
{

 
TI = 0; //清除串口1发送中断请求位

 
busy = 0; //清忙标志

 

 

 
}

 
if (RI) //检测串口1接收中断

 
{

 
RI = 0; //清除串口1接收中断请求位

 
P0 = SBUF; //P0显示串口数据 

 
SendData(P0);

 
}

 
}

 
/*----------------------------

 
发送串口数据

 
----------------------------*/

 
void SendData(BYTE dat)

 
{

 
 while (busy); //等待前面的数据发送完成

 
 busy = 1;

 
 SBUF = dat; //写数据到UART数据寄存器

 
}

 

 
/*----------------------------

 
发送字符串

 
----------------------------*/

 
void SendString(char *s)

 
{

 
 while (*s) //检测字符串结束标志

 
 {

 
 SendData(*s++); //发送当前字符

 
 }

 
}