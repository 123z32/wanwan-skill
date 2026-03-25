# 选择结构(if)

> 来源: OneNote > c语言 > 循环
> 修改: 2024-06-05T14:29:02Z

选择结构(if)
 
 
 
 
 

 

 
C语言中提供了两大选择结构, 分别是if和switch￼##选择结构if

 
if第一种形式

 
表示如果表达式为真,执行语句块1,否则不执行

 
if(表达式) {￼ 语句块1;￼}￼后续语句;

 
if(age >= 18) {￼ printf("开网卡\n");￼}￼printf("买烟\n");

 
if第二种形式

 
 
- 如果表达式为真,则执行语句块1,否则执行语句块2
 
- else不能脱离if单独使用
 

 
if(表达式){￼ 语句块1;￼}else{￼ 语句块2;￼}￼后续语句;

 
if(age > 18){￼ printf("开网卡\n");￼}else{￼ printf("喊家长来开\n");￼}￼printf("买烟\n");

 
if第三种形式

 
 
- 如果"表达式1"为真,则执行"语句块1",否则判断"表达式2",如果为真执行"语句块2",否则再判断"表达式3",如果真执行"语句块3", 当表达式1、2、3都不满足,会执行最后一个else语句
 
- 众多大括号中,只有一个大括号中的内容会被执行
 
- 只有前面所有添加都不满足, 才会执行else大括号中的内容
 

 
if(表达式1) {￼ 语句块1;￼}else if(表达式2){￼ 语句块2;￼}else if(表达式3){￼ 语句块3;￼}else{￼ 语句块4;￼}￼后续语句;

 
if(age>40){￼ printf("给房卡");￼}else if(age>25){￼ printf("给名片");￼}else if(age>18){￼ printf("给网卡");￼}else{￼ printf("给好人卡");￼}￼printf("买烟\n");

 
if嵌套

 
 
- if中可以继续嵌套if, else中也可以继续嵌套if
 

 
if(表达式1){￼ 语句块1;￼ if(表达式2){￼ 语句块2;￼ }￼}else{￼ if(表达式3){￼ 语句块3;￼ }else{￼ 语句块4;￼ }￼}

 

 
if注意点

 
 
- 任何数值都有真假性
 

 
#include <stdio.h>￼int main(){￼ if(0){￼ printf("执行了if");￼ }else{￼ printf("执行了else"); // 被执行￼ }￼}

 
当if else后面只有一条语句时, if else后面的大括号可以省略

 
 // 极其不推荐写法￼ int age = 17;￼ if (age >= 18)￼ printf("开网卡\n");￼ else￼ printf("喊家长来开\n");

 
当if else后面的大括号被省略时, else会自动和距离最近的一个if匹配

 
#include <stdio.h>￼int main(){￼ if(0)￼ if(1)￼ printf("A\n");￼ else // 和if(1)匹配￼ printf("B\n");￼ else // 和if(0)匹配, 因为if(1)已经被匹配过了￼ if (1)￼ printf("C\n"); // 输出C￼ else // 和if(1)匹配￼ printf("D\n");￼}

 
如果if else省略了大括号, 那么后面不能定义变量

 
#include <stdio.h>￼int main(){￼ if(1)￼ int number = 10; // 系统会报错￼ printf("number = %i\n", number);￼}

 
#include <stdio.h>￼int main(){￼ if(0){￼ int number = 10; ￼ }else￼ int value = 20; // 系统会报错￼ printf("value = %i\n", value);￼}

 
C语言中分号(;)也是一条语句, 称之为空语句

 
// 因为if(10 > 2)后面有一个分号, 所以系统会认为if省略了大括号￼// if省略大括号时只能管控紧随其后的那条语句, 所以只能管控分号￼if(10 > 2);￼{￼printf("10 > 2");￼}￼// 输出结果: 10 > 2

 
但凡遇到比较一个变量等于或者不等于某一个常量的时候，把常量写在前面

 
#include <stdio.h>￼int main(){￼ int a = 8;￼// if(a = 10){// 错误写法, 但不会报错￼ if (10 == a){￼ printf("a的值是10\n");￼ }else{￼ printf("a的值不是10\n");￼ }￼}