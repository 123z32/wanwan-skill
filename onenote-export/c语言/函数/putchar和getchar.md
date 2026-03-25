# putchar和getchar

> 来源: OneNote > c语言 > 函数
> 修改: 2024-05-24T03:06:55Z

putchar和getchar
 
 
 
 
 

 
putchar: 向屏幕输出一个字符

 
#include <stdio.h>

 
int main(){

 
 char ch = 'a';

 
 putchar(ch); // 输出a

 
}

 

 
getchar: 从键盘获得一个字符

 
#include <stdio.h>

 
int main(){

 
 char ch;

 
 ch = getchar();// 获取一个字符

 
 printf("ch = %c\n", ch);

 
}