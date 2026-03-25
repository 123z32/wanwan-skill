# sizeof运算符(计算内存字节数）

> 来源: OneNote > c语言 > 运算符
> 修改: 2024-06-04T13:44:04Z

sizeof运算符(计算内存字节数）
 
 
 
 
 

 

 
sizeof可以用来计算一个变量或常量、数据类型所占的内存字节数

 

 
标准格式: sizeof(常量 or 变量);

 
sizeof的几种形式

 

 
sizeof( 变量\常量 );

 
sizeof(10);

 
char c = 'a'; sizeof(c);

 

 
sizeof 变量\常量;

 
sizeof 10;

 
char c = 'a'; sizeof c;

 

 
sizeof( 数据类型);

 
sizeof(float);

 
如果是数据类型不能省略括号

 

 
sizeof面试题:

 

 
sizeof()和+=、*=一样是一个复合运算符, 由sizeof和()两个部分组成, 但是代表的是一个整体

 
所以sizeof不是一个函数, 是一个运算符, 该运算符的优先级是2

 
#include <stdio.h>

 
int main(){

 
 int a = 10;

 
 double b = 3.14;

 
 // 由于sizeof的优先级比+号高, 所以会先计算sizeof(a);

 
 // a是int类型, 所以占4个字节得到结果4

 
 // 然后再利用计算结果和b相加, 4 + 3.14 = 7.14

 
 double res = sizeof a+b;

 
 printf("res = %lf\n", res); // 7.14

 
}