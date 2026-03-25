# 选择结构(switch)

> 来源: OneNote > c语言 > 循环
> 修改: 2024-06-23T07:21:01Z

选择结构(switch)
 
 
 
 
 

 

 
由于 if else if 还是不够简洁，所以switch 就应运而生了，他跟 if else if 互为补充关系。switch 提供了点的多路选择

 
格式:

 
switch(表达式){

 
 case 常量表达式1:

 
 语句1;

 
 break;

 
 case 常量表达式2:

 
 语句2; 

 
 break;

 
 case 常量表达式n:

 
 语句n;

 
 break;

 
 default:

 
 语句n+1;

 
 break;

 
}

 
语义:

 
计算"表达式"的值, 逐个与其后的"常量表达式"值相比较,当"表达式"的值与某个"常量表达式"的值相等时, 即执行其后的语句, 然后跳出switch语句

 
如果"表达式"的值与所有case后的"常量表达式"均不相同时,则执行default后的语句

 
示例:

 
#include <stdio.h>

 

 
int main()

 
 {

 
 int num = 3;

 
 switch(num){

 
 case 1:

 
 printf("星期一\n");

 
 break;

 
 case 2:

 
 printf("星期二\n");

 
 break;

 
 case 3:

 
 printf("星期三\n");

 
 break;

 
 case 4:

 
 printf("星期四\n");

 
 break;

 
 case 5:

 
 printf("星期五\n");

 
 break;

 
 case 6:

 
 printf("星期六\n");

 
 break;

 
 case 7:

 
 printf("星期日\n");

 
 break;

 
 default:

 
 printf("回火星去\n");

 
 break;

 
 }

 
}

 
switch注意点

 
switch条件表达式的类型必须是整型, 或者可以被提升为整型的值(char、short)

 
#include <stdio.h>

 

 
int main() {

 

 
 switch(1.1){ // 报错

 
 case 1:

 
 printf("星期一\n");

 
 break;

 
 case 2:

 
 printf("星期二\n");

 
 break;

 
 default:

 
 printf("回火星去\n");

 
 break;

 
 }

 
}

 

 
case的值只能是常量, 并且还必须是整型, 或者可以被提升为整型的值(char、short)

 
#include <stdio.h>

 

 
int main() {

 

 
 int num = 3;

 
 switch(1){ 

 
 case 1:

 
 printf("星期一\n");

 
 break;

 
 case 'a':

 
 printf("星期二\n");

 
 break;

 
 case num: // 报错

 
 printf("星期三\n");

 
 break;

 
 case 4.0: // 报错

 
 printf("星期四\n");

 
 break;

 
 default:

 
 printf("回火星去\n");

 
 break;

 
 }

 
}

 
case后面常量表达式的值不能相同

 
#include <stdio.h>

 

 
int main() {

 
 switch(1){ 

 
 case 1: // 报错

 
 printf("星期一\n");

 
 break;

 
 case 1: // 报错

 
 printf("星期一\n");

 
 break;

 
 default:

 
 printf("回火星去\n");

 
 break;

 
 }

 
}

 
case后面要想定义变量,必须给case加上大括号

 
#include <stdio.h>

 

 
int main() {

 
 switch(1){

 
 case 1:{

 
 int num = 10;

 
 printf("num = %i\n", num);

 
 printf("星期一\n");

 
 break;

 
 }

 
 case 2:

 
 printf("星期一\n");

 
 break;

 
 default:

 
 printf("回火星去\n");

 
 break;

 
 }

 
}

 
switch中只要任意一个case匹配, 其它所有的case和default都会失效. 所以如果case和default后面没有 k就会出现穿透问题

 
#include <stdio.h>

 

 
int main() {

 

 
 int num = 2;

 
 switch(num){

 
 case 1:

 
 printf("星期一\n");

 
 break;

 
 case 2:

 
 printf("星期二\n"); // 被输出

 
 case 3:

 
 printf("星期三\n"); // 被输出

 
 default:

 
 printf("回火星去\n"); // 被输出

 
 break;

 
 }

 
}

 
switch中default可以省略

 
#include <stdio.h>

 

 
int main() {

 
 switch(1){

 
 case 1:

 
 printf("星期一\n");

 
 break;

 
 case 2:

 
 printf("星期一\n");

 
 break;

 
 }

 
}

 
switch中default的位置不一定要写到最后, 无论放到哪都会等到所有case都不匹配才会执行(穿透问题除外)

 
#include <stdio.h>

 

 
int main() {

 
 switch(3){

 
 case 1:

 
 printf("星期一\n");

 
 break;

 
 default:

 
 printf("Other,,,\n");

 
 break;

 
 case 2:

 
 printf("星期一\n");

 
 break;

 
 }

 
}