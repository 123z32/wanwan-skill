# 循环结构(do while)

> 来源: OneNote > c语言 > 循环
> 修改: 2024-06-06T13:48:23Z

循环结构(do while)
 
 
 
 
 

 
格式:

 
do {

 
 循环体中的语句;

 
 能够让循环结束的语句;

 
 ....

 
} while (循环控制条件 );

 
示例

 
int count = 0;

 
do {

 
 printf("发射子弹~哔哔哔哔\n");

 
 count++;

 
}while(count < 10);

 
do-while循环执行流程

 

 
首先不管while中的条件是否成立, 都会执行一次"循环体"

 
执行完一次循环体,接着再次判断while中的条件是否为真, 为真继续执行循环体,为假跳出循环

 
重复以上操作, 直到"循环控制条件"为假为止

 
应用场景

 

 
口令校验

 
#include<stdio.h>

 
int main()

 
{

 
 int num = -1;

 
 do{

 
 printf("请输入密码,验证您的身份\n");

 
 scanf("%d", &num);

 
 }while(123456 != num);

 
 printf("主人,您终于回来了\n");

 
}

 
while和dowhile应用场景

 
绝大多数情况下while和do while可以互换, 所以能用while就用while

 

 
无论如何都需要先执行一次循环体的情况, 才使用do while

 

 
do while 曾一度提议废除，但是他在输入性检查方面还是有点用的