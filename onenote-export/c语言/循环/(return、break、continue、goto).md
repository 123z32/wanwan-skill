# (return、break、continue、goto)

> 来源: OneNote > c语言 > 循环
> 修改: 2024-06-06T14:00:28Z

(return、break、continue、goto)
 
 
 
 
 

 
四大跳转

 
 
- C语言中提供了四大跳转语句, 分别是return、break、continue、goto
 
- 
break:

 
 
- 立即跳出switch语句或循环
 

 
 
- 
应用场景:

 
 
- switch
 
- 循环结构
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-2363479ae8394123a37a1bb5b7bd4de5!1-9E53C6D99C1E5AD1!263/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-7cd240bb5bb4490098f59d8dca868bbe!1-9E53C6D99C1E5AD1!263/$value)
 

 
 
- 
break注意点:

 
 
- break离开应用范围，存在是没有意义的
 

 
 

 

 
if(1) {￼ break; // 会报错￼}

 
 
- 在多层循环中,一个break语句只向外跳一层
 

 
while(1) {￼ while(2) {￼ break;// 只对while2有效, 不会影响while1￼ }￼ printf("while1循环体\n");￼}

 
 
- break下面不可以有语句，因为执行不到
 

 
while(2){￼ break;￼ printf("打我啊!");// 执行不到￼}

 

 
 
- 
continue

 
 
- 结束***本轮***循环，进入***下一轮***循环
 

 
 
- 
应用场景:

 
 
- 循环结构
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-1a5fe0718ebc4d058aa0ae258b217d9f!1-9E53C6D99C1E5AD1!263/$value)
 

 
 
- 
continue注意点:

 
 
- continue离开应用范围，存在是没有意义的
 

 
 

 
if(1) {￼ continue; // 会报错￼}

 

 
 
- 
goto

 
 
- 这是一个不太值得探讨的话题，goto 会破坏结构化程序设计流程，它将使程序
 
- 层次不清，且不易读，所以慎用
 
- goto 语句，仅能在本函数内实现跳转，不能实现跨函数跳转(短跳转)。但是他
 
- 在跳出多重循环的时候效率还是蛮高的
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-0b3e17b9f49d44d7b1417716c2535dc7!1-9E53C6D99C1E5AD1!263/$value)
 

 
 

 

 
#include <stdio.h>￼int main(){￼ int num = 0;￼// loop:是定义的标记￼loop:if(num < 10){￼ printf("num = %d\n", num);￼ num++;￼ // goto loop代表跳转到标记的位置￼ goto loop;￼ }￼}

 

 
#include <stdio.h>￼int main(){￼ while (1) {￼ while(2){￼ goto lnj;￼ }￼ }￼ lnj:printf("跳过了所有循环");￼}

 

 

 
 
- 
return

 
 
- 结束当前函数，将结果返回给调用者
 
- 不着急, 放一放,学到函数我们再回头来看它