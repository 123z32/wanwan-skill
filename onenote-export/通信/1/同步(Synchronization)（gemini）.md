# 同步(Synchronization)（gemini）

> 来源: OneNote > 通信 > 1
> 修改: 2025-12-07T12:19:44Z

同步(Synchronization)（gemini）
 
 
 
 
 

 
那我在接收端怎么知道相位跟频率呢

 

 
这是一个非常棒的问题！这触及了通信系统中最核心、也是最难的技术——同步 (Synchronization)。

 
简单来说：接收端刚开机时，它是完全不知道发送端的准确频率和相位的。

 
接收端必须像一个侦探一样，通过接收到的信号里的蛛丝马迹，把频率和相位“推算”出来。这个过程主要分为两个步骤：硬件下变频（大概对准）和软件同步（精确对准）。

 

 
1. 现实的残酷：两个时钟永远对不准

 
首先你得接受一个物理事实：世界上没有两个完全一样的晶振。

 
 
- 发送端 (Tx): 它的晶振说“我现在产生的是 2.400000000 GHz”。
 
- 接收端 (Rx): 它的晶振也设成了 2.4 GHz，但由于制造误差、温度影响，它实际产生的可能是 2.400000050 GHz。
 

 
这就产生了一个频率偏差 (CFO, Carrier Frequency Offset)。

 
这会导致什么后果？

 
回顾我们的复数符号 S。如果频率对不准，在星座图上，你的符号点就会旋转。

 
 
- 频率差一点点 →星座图在缓慢旋转。
 
- 频率差很多 →星座图飞速旋转，变成一个圆圈，根本看不出是 QPSK 还是 QAM。
 

 

 

 
2. 怎么“找”回频率和相位？（三大法宝）

 
在数字通信（特别是你用的 SDR/LabVIEW）中，我们通常使用以下几种方法来“知道”相位和频率：

 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-3f96ec0c0aef41998916e8a148bbaae6!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-9f37eaa3afbc4e6c9211fffdb0a6ae82!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-37d0b58c74e5436a9ba02dddb3fb0a19!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-1aeceb1160284c55bb44b031250d379a!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
总结

 
你不需要在物理上“知道”绝对的相位和频率，你只需要测量出“接收到的信号”和“标准信号”之间的差值，然后用数学方法把这个差值补偿掉。