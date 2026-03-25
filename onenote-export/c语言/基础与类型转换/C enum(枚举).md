# C enum(枚举)

> 来源: OneNote > c语言 > 基础与类型转换
> 修改: 2025-12-28T06:17:00Z

C enum(枚举)
 
 
 
 
 

 
枚举是 C 语言中的一种基本数据类型，用于定义一组具有离散值的常量，它可以让数据更简洁，更易读。

 
枚举类型通常用于为程序中的一组相关的常量取名字，以便于程序的可读性和维护性。

 
定义一个枚举类型，需要使用 enum 关键字，后面跟着枚举类型的名称，以及用大括号 {} 括起来的一组枚举常量。每个枚举常量可以用一个标识符来表示，也可以为它们指定一个整数值，如果没有指定，那么默认从 0 开始递增。

 

 
枚举语法定义格式为：

 
enum　枚举名　{枚举元素1,枚举元素2,……};

 

 
例子：比如：一星期有 7 天，如果不用枚举，我们需要使用 #define 来为每个整数定义一个别名：

 
#define MON 1 

 
#define TUE 2 

 
#define WED 3

 
#define THU 4 

 
#define FRI 5 

 
#define SAT 6 

 
#define SUN 7

 
这个看起来代码量就比较多，接下来我们看看使用枚举的方式：

 
enum DAY￼{￼ MON=1, TUE, WED, THU, FRI, SAT, SUN￼};

 

 
注意：第一个枚举成员的默认值为整型的 0，后续枚举成员的值在前一个成员上自动加 1。我们在这个实例中把第一个枚举成员的值定义为 1，第二个就为 2，以此类推。

 

 
枚举变量的定义

 
前面我们只是声明了枚举类型，接下来我们看看如何定义枚举变量。

 
我们可以通过以下三种方式来定义枚举变量

 
1、先定义枚举类型，再定义枚举变量

 
enum DAY￼{￼ MON=1, TUE, WED, THU, FRI, SAT, SUN￼};￼enum DAY day;

 
2、定义枚举类型的同时定义枚举变量（类似结构体）

 
enum DAY￼{￼ MON=1, TUE, WED, THU, FRI, SAT, SUN￼} day;

 
3、省略枚举名称，直接定义枚举变量

 
enum￼{￼ MON=1, TUE, WED, THU, FRI, SAT, SUN￼} day;

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 
参考示例

 
实例

 
#include <stdio.h> 

 
enum DAY 

 
{ 

 
MON=1, TUE, WED, THU, FRI, SAT, SUN 

 
}; 

 
int main() 

 
{ 

 
enum DAY day; 

 
day = WED; 

 
printf("%d",day); 

 
return 0; 

 
}

 
以上实例输出结果为：

 
3

 

 
在C 语言中，枚举类型是被当做 int 或者 unsigned int 类型来处理的，所以按照 C 语言规范是没有办法遍历枚举类型的。

 
不过在一些特殊的情况下，枚举类型必须连续是可以实现有条件的遍历。

 
以下实例使用 for 来遍历枚举的元素：

 
实例

 
#include <stdio.h> enum DAY 

 
{

 
 MON=1, TUE, WED, THU, FRI, SAT, SUN

 
 } day; 

 
int main() 

 
{ 

 
// 遍历枚举元素 for (day = MON; day <= SUN; day++) 

 
{

 
 printf("枚举元素：%d \n", day);

 
 } 

 
}

 
以上实例输出结果为：

 
枚举元素：1 ￼枚举元素：2 ￼枚举元素：3 ￼枚举元素：4 ￼枚举元素：5 ￼枚举元素：6 ￼枚举元素：7

 
以下枚举类型不连续，这种枚举无法遍历。

 
enum￼{￼ ENUM_0,￼ ENUM_10 = 10,￼ ENUM_11￼};

 
枚举在 switch 中的使用：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-2119b74d05d94a2093af259381221282!1-9E53C6D99C1E5AD1!264/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-84304d0d4d494ccaa85633a5c55ef6f8!1-9E53C6D99C1E5AD1!264/$value)