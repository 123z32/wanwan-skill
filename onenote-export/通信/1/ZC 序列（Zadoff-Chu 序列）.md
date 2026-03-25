# ZC 序列（Zadoff-Chu 序列）

> 来源: OneNote > 通信 > 1
> 修改: 2025-12-22T12:32:53Z

ZC 序列（Zadoff-Chu 序列）
 
 
 
 
 

 
ZC 序列（Zadoff-Chu 序列）是一种具有良好性质的离散序列，它是一种复数序列，在通信系统中广泛应用。它由 Zadoff 和 Chu 于 1964 年提出，是一种特殊的线性调频脉冲压缩序列。ZC 序列常用于通信系统中的同步和信道估计等方面。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-56f46ff68ec94d09b6c2e62fe31cbd28!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
核心参数：

 
根索引（root index）：对应上图中物理根序列号u,u是由逻辑根序列号查表获取；

 
ZC 序列的长度：对应上图中根序列长度LRA一定得是奇数（常常是质数）；

 
性质 1：恒包络，即等模

 
任意长度的 ZC 序列幅值恒定，这也意味着功率恒定，这个好处就是射频器件不用忽大忽小的改变放大能量。有利于射频功放信号发挥最大的效率

 
性质 2：零循环自相关

 
一个 ZC序列的循环自相关是最优的，因为对于所有的非零移位序列，与原序列的自相关都等于 0

 
(序列移位后与原序列不相关)

 
性质 3：固定循环互相关

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-0cb31607f79c45d190f940d6402b98ed!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
（不同 “根索引” 的 ZC 序列，互相干扰小）

 
性质 4：傅里叶变换后仍是 ZC 序列

 
适配主流通信系统