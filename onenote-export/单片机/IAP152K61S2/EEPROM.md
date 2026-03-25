# EEPROM

> 来源: OneNote > 单片机 > IAP152K61S2
> 修改: 2025-06-14T16:43:48Z

EEPROM
 
 
 
 
 

 
注意写入数据需要关闭中断

 
以免影响写入

 

 
Extern u8 R_data

 

 
//AT24C02_wrtie(0X00,0X00);//初始化

 
EEPROM=AT24C02_read(0x00);//读取数据

 
Delay10ms();

 
EEPROM++;

 
Delay10ms();

 

 
AT24C02_wrtie(0x00,EEPROM);//写入+1开机数据

 
Delay10ms();

 

 
smg_buffer[0]=EEPROM/100;

 
smg_buffer[1]=EEPROM%100/10;

 
smg_buffer[2]=EEPROM%10;

 

 
EA=1;

 
while(1);

 

 
void AT24C02_wrtie(unsigned char add,unsigned char W_data)

 
{

 
I2CStart();//

 
I2CSendByte(0XA0);

 
I2CWaitAck();

 
I2CSendByte(add);

 
I2CWaitAck();

 
I2CSendByte(W_data);

 
I2CWaitAck();

 
I2CStop();

 
Delay10ms1();

 
}

 
Void AT24C02_read(unsigned char add)

 
{

 

 
I2CStart();

 
I2CSendByte(0XA0);

 
I2CWaitAck();

 
I2CSendByte(add);

 
I2CWaitAck();

 

 
I2CStart();

 
I2CSendByte(0XA1);

 
I2CWaitAck();

 
R_data=I2CReceiveByte(）;

 
I2CSendAck(1);

 
I2CStop();

 

 
}

 

 
#ifndef _iic_h

 
#define _iic_h

 
#include <STC15F2K60S2.H>

 
#include <intrins.h>

 

 
static void I2C_Delay(unsigned char n);

 
void I2CStart(void);

 
void I2CStop(void);

 
void I2CSendByte(unsigned char byt);

 
unsigned char I2CReceiveByte(void);

 
unsigned char I2CWaitAck(void);

 
void I2CSendAck(unsigned char ackbit);

 
void AT24C02_wrtie(unsigned char add,unsigned char W_data);

 
unsigned char AT24C02_read(unsigned char add);

 

 
sbit sda=P2^1;

 
sbit scl=P2^0;

 

 
#endif