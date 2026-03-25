# KEY

> 来源: OneNote > 单片机 > IAP152K61S2
> 修改: 2025-06-11T08:39:58Z

KEY
 
 
 
 
 

 
#include <public.H>

 
#include <key.H>

 

 
u8 key=0;

 
u8 key_value=0;

 
sbit col1=P4^4;sbit col2=P4^2;sbit col3=P3^5;sbit col4=P3^4;

 

 
////独立按键

 
//u8 key_scan(void)

 
//{

 
// key_value=0;

 
// P3=0XFF;col1=0;col2=1;col3=1;col4=1;

 
// if((P3&0X0F)!=0X0F)

 
// {

 
// switch(P3&0X0F)

 
// {

 
// case 0x0E:key_value=7;break; 

 
// case 0x0D:key_value=6;break;

 
// case 0x0B:key_value=5;break;

 
// case 0x07:key_value=4;break;

 
// }

 
// }

 
// if(key_value!=0)key++;

 
// else key=0;

 
// if(key>=20)return key_value*5;//*5才不会碰到4-19

 
// else if(key>=3)return key_value;

 
// else return key_value;

 
//}

 

 
//矩阵按键

 
u8 key_scan(void)

 
{

 
key_value=0;

 
P3=0XFF;col1=0;col2=1;col3=1;col4=1;

 
if((P3&0X0F)!=0X0F)

 
{

 
switch(P3&0X0F)

 
{

 
case 0x0E:key_value=7;break; 

 
case 0x0D:key_value=6;break;

 
case 0x0B:key_value=5;break;

 
case 0x07:key_value=4;break;

 
}

 
}

 
P3=0XFF;

 
col1=1;col2=0;col3=1;col4=1;

 
if((P3&0X0F)!=0X0F)

 
{

 
switch(P3&0X0F)

 
{

 
case 0x0E:key_value=11;break;

 
case 0x0D:key_value=10;break;

 
case 0x0B:key_value=9;break;

 
case 0x07:key_value=8;break;

 
}

 
}

 
P3=0XFF;

 
col1=1;col2=1;col3=0;col4=1;

 
if((P3&0XDF)!=0XDF)

 
{

 
switch(P3&0XDF)

 
{

 
case 0xDE:key_value=15;break;

 
case 0xDD:key_value=14;break;

 
case 0xDB:key_value=13;break;

 
case 0xD7:key_value=12;break;

 
}

 
}

 

 
P3=0XFF;

 
col1=1;col2=1;col3=1;col4=0;

 
if((P3&0XEF)!=0XEF)

 
{

 
switch(P3&0XEF)

 
{

 
case 0xEE:key_value=19;break;

 
case 0xED:key_value=18;break; 

 
case 0xEB:key_value=17;break;

 
case 0xE7:key_value=16;break;

 
}

 
}

 

 
if(key_value!=0)key++;

 
else key=0; 

 
if(key>=20)return key_value*5;//*5才不会碰到4-19 长按功能 10ms*20等于200ms

 
else if(key>=3)return key_value;

 
else return key_value;

 
}