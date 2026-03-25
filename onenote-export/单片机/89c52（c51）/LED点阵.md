# LED点阵

> 来源: OneNote > 单片机 > 89c52（c51）
> 修改: 2024-09-08T10:16:43Z

LED点阵
 
 
 
 
 

 
LED 点阵是由发光二极管排列组成的显示器件,在我们日常生活的电器中随 处可见，被广泛应用于汽车报站器，广告屏等。如下所示：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-98ad377032cb44afa7a1360fb5397e40!1-9E53C6D99C1E5AD1!269/$value)
 
 通常应用较多的是 8*8 点阵，然后使用多个 8*8 点阵可组成不同分辨率的 LED 点阵显示屏，比如 16*16 点阵可以使用 4 个 8*8 点阵构成。因此理解了 8*8LED 点阵的工作原理，其他分辨率的 LED点阵显示屏都是一样的。这里以8*8LED 点阵来做介绍。其内部结构图如下所示：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-1f2ed47bb55e48f19139d210c38b64b6!1-9E53C6D99C1E5AD1!269/$value)
 
 8*8 点阵共由64个发光二极管组成，且每个发光二极管是放置在行线和列线 的交叉点上，当对应的某一行置 1 电平，某一列置 0 电平，则相应的二极管就亮； 如要将第一个点点亮，则 1 脚接高电平 a 脚接低电平，则第一个点就亮了；如果 要将第一行点亮，则第 1 脚要接高电平，而（a、b、c、d、e、f、g、h ）这些 引脚接低电平，那么第一行就会点亮；如要将第一列点亮，则第 a 脚接低电平， 而（1、2、3、4、5、6、7、8）接高电平，那么第一列就会点亮。由此可见，LED 点阵的使用也是非常简单的。 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-776f179637064ef3942ecbd839f2621c!1-9E53C6D99C1E5AD1!269/$value)
 
LED 点阵（点亮一个点)

 
#include <REGX52.H>

 

 
typedef unsigned int u16;

 
typedef unsigned char u8;

 

 
#define LEDDA_COL_PORT P0

 

 
sbit SER=P3^4;

 
sbit RCLK1=P3^5;

 
sbit SRCLK=P3^6;

 

 
u8 LEDDA1[8]={0X01,0X02,0X04,0X08,0X10,0X20,0X40,0X80};

 

 
void ms(u16 t)

 
{

 
u8 i=0;

 
while(t--)for(i=0;i<123;i++);

 

 
}

 

 
void us(u16 k)

 
{

 
while(k--);

 
}

 

 
void HC595(u8 j)

 
{

 
u8 i=0;

 
for(i=0;i<8;i++)

 
{ 

 
SER=j>>7;

 
j<<=1;

 
SRCLK=0;

 
us(1);

 
SRCLK=1;

 
}

 
RCLK1=0;

 
us(1);

 
RCLK1=1;

 
}

 

 
int main()

 
{

 
u8 i=0;

 
LEDDA_COL_PORT=~0X80;

 
HC595(0x00);

 
HC595(LEDDA1[7]);

 
}

 

 

 
点亮一个点很简单，可是如何点亮多个点呢？如果需要一次显示多个怎么 办？从原理图上可以看到每一行上都连接着多个 LED 灯，每一列上也都连接着多个 LED 灯，如果要点亮一个，按照上面原理可以，但是要同时点亮多个怎么办？

 
 那么就需要用到动态数码管的动态扫描原理。首先如何点亮一行上面多个灯或者一列上面多个灯？明显需要某行或某列有效，同时使多列或多行有效。比如 在第一行有效（输出高电平）的情况下，有效列（输出低电平）与这一行交点上 的 LED 灯就会被点亮。那么实现一行或一列点亮会比较容易。如何实现不同行 不同列上的灯被多个点亮呢？ 是否是行有效，列有效就可以？并不是！

 
 要实现行列不同位置亮灯，需要使用动态显示的方法，也要结合扫描的方法。 在第一行亮灯一段时间以后灭掉，点亮第二行一段时间以后灭掉，点亮第三行一 段时间以后灭掉，如此点亮，直到八行全部点亮一次，在第一行点亮到最后一行灭掉的总时间不能超过人肉眼可识别的时间，即 24 毫秒。在每一行点亮的时候， 给列一个新的数据，此时对应列的数据就可以体现在这行上要点亮的灯上。这样 就和动态数码管的显示一样，只不过数码管的 LED 灯是段值。这里使用 LED点阵显示数字，也是多个 LED 同时点亮。

 
 要想在点阵上显示数字等字符，首先要获取在 LED 点阵上显示数字字符所需 的数据，即一个数字字符在 LED 点阵上显示，对应的每行每列都会有一些灯点亮 或者熄灭，这样就会构成一组数据，也就是数字字符的显示数据，我们只要将这 些数据通过 74HC595 发送到点阵对应的行或列就能显示数字字符。 

 
 数字字符数据如何获取呢？这里给大家介绍一个非常好用的工具-取字模软 件。该软件在“\5--开发工具\4-常用辅助开发软件\文字取模软件”内，如下所 示

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-d7a7c48164cf45c6a8d4f156af9dd031!1-9E53C6D99C1E5AD1!269/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-ed52ebb7869b4102b297bcd368268a4c!1-9E53C6D99C1E5AD1!269/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-f735dc29fc194f4ea9463eb092b5030d!1-9E53C6D99C1E5AD1!269/$value)
 

 
LED点阵（显示数字）

 
#include <REGX51.H>

 

 
typedef unsigned int u16;//对系统默认数据类型进行重定义

 
typedef unsigned char u8;

 

 
#define LEDDZ_COL_PORT P0

 
//定义 74HC595 控制管脚

 
sbit SER=P3^4;

 
sbit RCLK=P3^5;

 
sbit SRCLK=P3^6;

 

 
u8 GLED_COL[8]={0x00,0x7C,0x82,0x82,0x82,0x7C,0x00,0x00};//LED 点阵显示数字 0 的行数据

 
u8 GLED_ROW[8]={0x7f,0xbf,0xdf,0xef,0xf7,0xfb,0xfd,0xfe};//LED 点阵显示数字 0 的列数据

 

 

 
void us(u16 t)

 
{ 

 
while(t--);

 
}

 

 
void ms(u16 k)

 
{

 
u8 i=0;

 
while(k--)for(i=0;i<123;i++);

 
}

 

 
void HC595(u8 dat)

 
{

 
u8 i=0;

 
for(i=0;i<8;i++)

 
{

 
SER=dat>>7;

 
dat<<=1;

 
SRCLK=0;

 
us(1);

 
SRCLK=1;

 
}

 
RCLK=0;

 
us(1);

 
RCLK=1;

 
}

 

 
int main()

 
{

 
u8 i=0;

 
while(1)

 
{

 
for(i=0;i<8;i++)//循环 8 次扫描 8 行、列

 
{

 
LEDDZ_COL_PORT=GLED_ROW[i];//传送列选数据

 
HC595(GLED_COL[i]);//传送行选数据

 
ms(10);//延时一段时间，等待显示稳定

 
HC595(0X00);//消影

 
}

 
}

 
}

 
LED 点阵（显示图像）

 
#include <REGX51.H>

 

 
typedef unsigned int u16;//对系统默认数据类型进行重定义

 
typedef unsigned char u8;

 

 
#define LEDDZ_COL_PORT P0

 
//定义 74HC595 控制管脚

 
sbit SER=P3^4;

 
sbit RCLK=P3^5;

 
sbit SRCLK=P3^6;

 

 
u8 GLED_COL[8]={0x38,0x7C,0x7E,0x3F,0x3F,0x7E,0x7C,0x38};//LED 点阵显示数字 0 的行数据 爱心数据

 
u8 GLED_ROW[8]={0x7f,0xbf,0xdf,0xef,0xf7,0xfb,0xfd,0xfe};//LED 点阵显示数字 0 的列数据

 

 

 
void us(u16 t)

 
{ 

 
while(t--);

 
}

 

 
void ms(u16 k)

 
{

 
u8 i=0;

 
while(k--)for(i=0;i<123;i++);

 
}

 

 
void HC595(u8 dat)

 
{

 
u8 i=0;

 
for(i=0;i<8;i++)

 
{

 
SER=dat>>7;

 
dat<<=1;

 
SRCLK=0;

 
us(1);

 
SRCLK=1;

 
}

 
RCLK=0;

 
us(1);

 
RCLK=1;

 
}

 

 
int main()

 
{

 
u8 i=0;

 
while(1)

 
{

 
for(i=0;i<8;i++)//循环 8 次扫描 8 行、列

 
{

 
LEDDZ_COL_PORT=GLED_ROW[i];//传送列选数据

 
HC595(GLED_COL[i]);//传送行选数据

 
us(1);//延时一段时间，等待显示稳定

 
HC595(0X00);//消影

 
}

 
}

 
}