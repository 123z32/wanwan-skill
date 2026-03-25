# WiFi (802.11) 协议的同步模块（gemini）

> 来源: OneNote > 通信 > 1
> 修改: 2025-12-07T12:35:50Z

WiFi (802.11) 协议的同步模块（gemini）
 
 
 
 
 

 

 

 

 
这将涵盖两个核心部分：“甜甜圈”效应（问题的直观展示） 和 前导码（Preamble）机制（解决问题的手段）

 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-91454f9e20ba4581ba82e2e69c225f6c!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-ca4288282cfe462db08e02b0f45758dc!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-b5be7e924f3f4535afd37e306c88ea55!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-d5bb04111c414f8e8adc9691520b4cd7!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-6b983f77622b4819a37a9aeffd238b46!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
我们在接收端“知道”相位和频率，不是靠猜，而是靠测量重复信号的相位差。

 
 
- 现象： 频率不对→星座图变甜甜圈。
 
- 手段： 发送重复的 Preamble（前导码）。
 
- 计算： 比较重复部分之间的相位转角→算出频率偏差→补偿回去