# 利用KELE软件仿真查找延时时间

> 来源: OneNote > 单片机 > 89c52（c51）
> 修改: 2024-08-21T12:50:02Z

利用KELE软件仿真查找延时时间
 
 
 
 
 

 
#include <reg52.h>

 
typedef unsigned int u16;

 
typedef unsigned char u8;

 
sbit LED1=P2^0;

 
/********************************************************************

 
* 函 数 名 : delay_10us

 
* 函数功能 : 延时函数，ten_us=1 时，大约延时 10us

 
* 输 入 : ten_us

 
* 输 出 : 无

 
*********************************************************************/

 

 
void delay_10us (u16 ten_us)//延时1

 
{

 
while(ten_us--);

 
}

 

 
void delay_ms(u16 t)//延时2

 
{

 
u8 i;

 
while(t--)for(i=0;i<123;i++);

 
} 

 
/*void delay_ms(unsigned int t)//延时3

 
{

 
unsigned char i;

 
while (t--)for(i=0;i<123;i++);

 
}*/

 

 
void main()

 
{

 
LED1=1;

 
while(1)

 
{

 
LED1=0;

 
delay_10us(50000);//大约480ms

 
LED1=1;

 
delay_ms(450);

 
}

 
}

 
上述代码延时1中我们传递实参是 50000，得到的延时大约是 450ms，如何来验证 呢？可以通过 KEIL 自带的软件仿真功能，操作如下： ①打开实验工程，点击魔术棒，选择“Target”选项卡，在 Xtal(MHz)文本 框中输入 12M，该值表示开发板上实际使用外部晶振大小，如果开发板上使用外 部晶振是 11.0592M，则修改为对应值。然后点击 Ok。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-09bd5e35afad4325b0c742587272e2cd!1-9E53C6D99C1E5AD1!269/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-a6d67df1b7ac4c85933cc6a1e59f9d71!1-9E53C6D99C1E5AD1!269/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-60b1faffdf9b48d5ac0d7aa038752ee9!1-9E53C6D99C1E5AD1!269/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-52d11220a91642a3bddc853c80201ad1!1-9E53C6D99C1E5AD1!269/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-8faa48a6a3434fb0b8d717d66015d5a6!1-9E53C6D99C1E5AD1!269/$value)