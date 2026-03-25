# SMG

> 来源: OneNote > 单片机 > IAP152K61S2
> 修改: 2025-06-06T05:13:15Z

SMG
 
 
 
 
 

 
#ifndef __SMG_H__

 
#define __SMG_H__

 

 
void smg_xs();//数码管显示

 
extern u8 jm;

 
extern u8 smgbuf[4][8]; 

 
#endif

 

 
#include <public.h>

 
#include <smg.H>

 
sbit DP=P0^7;//小数点引脚

 
code u8 tab[]={0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,

 
0x88,0x83,0xc6,0xa1,0x86,0x8e,

 
0xff,0xbf,0xc1}; 

 
u8 smg_wei=0;

 

 

 
u8 jm=0; 

 
u8 smgbuf[4][8]={{18,1,15,15,15,15,15,15},

 
 {18,2,16,16,16,17,16,16},

 
 {18,3,16,16,16,16,16,16},

 
 {18,4,15,15,15,15,15,15}};

 

 
void smg_xs()//数码管多界面显示函数

 
{

 
if (smg_wei==8)smg_wei=0;

 
P2=((P2&0X1F)|0XE0);

 
switch(jm)

 
{

 
case 0:P0=tab[smgbuf[0][smg_wei]];break;//case 0:P0=tab[smgbuf1[smg_wei]];//if(smg_wei==6)DP=0;break;加小数点示范

 
case 1:P0=tab[smgbuf[1][smg_wei]];break;

 
case 2:P0=tab[smgbuf[2][smg_wei]];break;

 
case 3:P0=tab[smgbuf[3][smg_wei]];break;

 
}

 
P2&=0x1f;

 
P2=((P2&0X1F)|0XC0);

 
P0=0X01<<smg_wei;

 
P2&=0x1f;

 
smg_wei++;

 
}

 

 

 
//void smg_xs()//数码管单界面显示函数

 
//{

 
// if (smg_wei==8)smg_wei=0;

 
// P2=((P2&0X1F)|0XE0);

 
// P0=tab[smgbuf1[smg_wei]];

 
// P2=((P2&0X1F)|0XC0);

 
// P0=0X01<<smg_wei;

 
// P2&=0x1f;

 
// smg_wei++;

 
//}