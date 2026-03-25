# LED

> 来源: OneNote > 单片机 > IAP152K61S2
> 修改: 2025-06-06T08:57:42Z

LED
 
 
 
 
 

 

 

 

 
 

 
void LED(u8 LEDBUF)//0XFF全亮//0X00全灭

 
{

 
P2=P2&0X1F|0X80;

 
P0=LEDBUF;

 
P2=P2&0X1F;

 
}