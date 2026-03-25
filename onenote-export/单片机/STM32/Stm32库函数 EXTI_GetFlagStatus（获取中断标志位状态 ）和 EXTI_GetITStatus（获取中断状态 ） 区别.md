# Stm32库函数 EXTI_GetFlagStatus（获取中断标志位状态 ）和 EXTI_GetITStatus（获取中断状态 ） 区别

> 来源: OneNote > 单片机 > STM32
> 修改: 2024-06-09T10:48:11Z

Stm32库函数 EXTI_GetFlagStatus（获取中断标志位状态 ）和 EXTI_GetITStatus（获取中断状态 ） 区别
 
 
 
 
 

 

 
FlagStatus EXTI_GetFlagStatus(uint32_t EXTI_Line) //（获取中断标志位状态 ）

 
{

 
 FlagStatus bitstatus = RESET;

 
 /* Check the parameters */

 
 assert_param(IS_GET_EXTI_LINE(EXTI_Line));

 
 

 
 if ((EXTI->PR & EXTI_Line) != (uint32_t)RESET)

 
 {

 
 bitstatus = SET;

 
 }

 
 else

 
 {

 
 bitstatus = RESET;

 
 }

 
 return bitstatus;

 
}

 

 

 

 
ITStatus EXTI_GetITStatus(uint32_t EXTI_Line) //（获取中断状态 ）

 
{

 
 ITStatus bitstatus = RESET;

 
 uint32_t enablestatus = 0;

 
 /* Check the parameters */

 
 assert_param(IS_GET_EXTI_LINE(EXTI_Line));

 
 

 
 enablestatus = EXTI->IMR & EXTI_Line;

 
 if (((EXTI->PR & EXTI_Line) != (uint32_t)RESET) && (enablestatus != (uint32_t)RESET))

 
 {

 
 bitstatus = SET;

 
 }

 
 else

 
 {

 
 bitstatus = RESET;

 
 }

 
 return bitstatus;

 
}

 

 
可以很容易看出来，代码上的区别在：

 

 
EXTI_GetFlagStatus 部分：

 
if ((EXTI->PR & EXTI_Line) != (uint32_t)RESET)

 

 
EXTI_GetITStatus 部分：

 
enablestatus = EXTI->IMR & EXTI_Line;

 
if (((EXTI->PR & EXTI_Line) != (uint32_t)RESET) && (enablestatus != (uint32_t)RESET))

 

 
即 EXTI_GetITStatus 的判断多了一个条件。

 

 
由手册可以知道：

 

 
EXTI->PR 是 挂起寄存器，0：没有发生触发请求；1：发生了选择的触发请求

 
EXTI->IMR 是 中断屏蔽寄存器，0：屏蔽来自线x上的中断请求； 1：开放来自线x上的中断请求。

 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-ae96db59f7d24813b7a5e295945ca2b1!1-9E53C6D99C1E5AD1!270/$value)
 

 
因此，EXTI_GetFlagStatus 只是纯粹读取中断标志位的状态，但是实际上这并不准确，因为设置 EXTI_IMR 寄存器可以对该中断进行屏蔽；而 EXTI_GetITStatus 除了读取中断标志位，还查看 EXTI_IMR 寄存器是否对该中断进行屏蔽。

 

 
另外，EXTI_ClearFlag 和 EXTI_ClearITPendingBit 则是什么区别都没有，内部代码完全一样。