# LED

> 来源: OneNote > 单片机 > 89c52（c51）
> 修改: 2024-09-02T11:45:09Z

LED
 
 
 
 
 

 
LED 即发光二极管。它具有单向导电性，通过 5mA 左右电流即可发光，电流越大，其亮度越强，但若电流过大，会烧毁二极管，一般我们控制在 3 mA-20mA 之间，通常我们会在 LED 管脚上串联一个电阻，目的就是为了限制通过发光二极管的电流不要太大，因此这些电阻又可以称为“限流电阻”。当发光二极管发光 时，测量它两端电压约为 1.7V，这个电压又叫做发光二极管的“导通压降”。下图左右分别为直插式发光二极管和贴片式发光二极管实物图。发光二极管正极又称阳极，负极又称阴极，电流只能从阳极流向阴极。直插式发光二极管长脚为阳极，短脚为阴极。仔细观察贴片式发光二极管正面的一端有彩色标记，通常有标记的一端为阴极。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-276805ea096c49ce90a679d2feb60214!1-9E53C6D99C1E5AD1!269/$value)
 
LED模块电路

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-769fb9df083b4551a3d8020bc5885669!1-9E53C6D99C1E5AD1!269/$value)
 
点亮一个LED

 
#include "reg52.h"

 
 

 
sbit LED1=P2^0;

 

 
Void main()

 
{

 
LED1=0;

 
While(1)

 
{

 

 
}

 
}

 

 
LED闪烁

 
延时函数

 
/********************************************************************

 
* 函 数 名 : delay_10us

 
* 函数功能 : 延时函数，ten_us=1 时，大约延时 10us

 
* 输 入 : ten_us

 
* 输 出 : 无

 
*********************************************************************/

 

 
void delay_10us (u16 ten_us)

 
{

 
while(ten_us--);

 
}

 
上述代码即为延时函数，通过 while 循环来实现。函数入口有一个形式参数 ten_us，如果 ten_us 等于1，则 while 循环执行一次，调用该函数延时时间大约 10us，当然使用循环来实现延时，这种延时是不精确的，目前我们先得到个大概的时间即可。

 
 细心的朋友可能会看到函数形参 ten_us 是 u16 类型的，这个似乎不是C语言数据类型关键字，这是我们重定义的数据类型，如下： typedef unsigned int u16; //对系统默认数 据类型进行重命名 

 
typedef unsigned char u8; 使用关键字 

 

 
typedef 对系统默认数据类型 unsigned int 和 unsigned char 重新命名，主要是方便我们代码的书写和变量类型的查看。u16 即代表该变量是 16 位的无符号整型数据，u8 代表该变量是 8 位的无符号字符型数据。有了这个 就知道参数的传送范围，不能超过形参定义的范围

 

 
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

 

 
LED流水灯

 
根据流水灯实现 原理，即 IO 口由低往高或者由高往低逐个输出低电平特点，那么我们可以将移位操作以及循环结合进来。

 
#include <reg52.h>

 
#define LED_PORT P2//使用宏定义 P2 端口

 
//LED_PORT等于P2

 
typedef unsigned int u16;

 
typedef unsigned char u8;

 

 
void delay_ms(u16 t)

 
{

 
u8 i;

 
while(t--)for(i=0;i<123;i++);

 
}

 

 
void main()

 
{

 
u8 i=0;

 
while (1)

 
{

 
for(i=0;i<8;i++)

 
{

 
LED_PORT =~(0x01<<i);//将1右移i位，然后取

 
反将结果赋值到 LED_PORT

 
//LED_PORT =~(0x80>>i);//将1左移i位，

 
delay_ms(500);

 
}

 
}

 
}

 
进入 main 函数后首先定义一个变量 i，然后进入 while 循环，由于要实现 8 个 LED 从 D1->D8 循环点亮，因此可以使用 for 循环语句循环 8 次，每循环一次， 点亮的小灯向右移动一个，而 D1-D8 是连接到 P2.0-P2.7 的，因此输出的低电平 要左移一位，因此可以使用LED_PORT=~(0x01<<i);语句实现。0X01<<i表示i增加1次，0x01中的1就移动多少位，因为1（高电平）不会让 LED 点亮，需要取反后变为低电平0才能点亮，所以最后的结果需要取反后给 LED_PORT口，并且每次循环都要延时一段时间，这样才能分辨出来LED在流水。

 
LED循环灯

 
使用左移_crol_、右移_cror_函数 

 
除了使用 for 循环语句实现移位，KEIL C51 软件内还有对应的移位库函数， 左移函数是_crol_()，右移函数是_cror_()，要使用这两个函数在我们的程序中 必须包含 intrins.h 头文件。这两个移位函数大家可以百度了解下，其内部实现 过程是看不到的，该移位函数实现的移位功能就相当于一个队列内循环移动，如 果是左移，那么最高位就被移到最低位了，次高位变为最高位，依次类推。使用 左移、右移函数实现的流水灯操作代码如下

 

 
#include <reg52.h>

 
#include <intrins.h>

 
#define LED_PORT P2//使用宏定义 P2 端口

 

 
typedef unsigned int u16;

 
typedef unsigned char u8;

 

 
void delay_ms(u16 t)

 
{

 
u8 i;

 
while(t--)for(i=0;i<123;i++);

 
}

 

 
void main()

 
{

 
u8 i=0;

 
LED_PORT=~0x01;

 
delay_ms(500);

 
while(1)

 
{

 
for(i=0;i<7;i++)

 
{

 
LED_PORT=_crol_(LED_PORT,1);

 
delay_ms(500);

 
}

 
for(i=0;i<7;i++)

 
{

 
LED_PORT=_cror_(LED_PORT,1);

 
delay_ms(500);

 
}

 
}

 
}