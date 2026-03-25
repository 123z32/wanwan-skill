# 信道均衡（线性：ZF和MMSE，非线性：MLO和V-BLAST）

> 来源: OneNote > 通信 > 1
> 修改: 2025-12-09T08:02:33Z

信道均衡（线性：ZF和MMSE，非线性：MLO和V-BLAST）
 
 
 
 
 

 
 
信道均衡技术（Channel equalization）是指为了提高衰落信道中的通信系统的传输性能而采取的一种抗衰落措施。它主要是为了消除或者是减弱宽带通信时的多径时延带来的码间串扰ISI问题。

 
大体上分为两大类：线性与非线性均衡。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-8569497cdbcd4c8e9192f83d643ae048!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
常用两种线性均衡算法：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-6c89b9973e194b69a74435180d88a8a3!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-92f1c615c87d413786b2b30efd2ef54c!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
两种非线性检测信道均衡算法：

 
全称：Vertical-Bell Laboratories Layered Space-Time (贝尔实验室分层空时结构) 核心思想：串行干扰消除 (SIC, Successive Interference Cancellation)。

 
- 每一层采用线性检测算法，比如ZF、MMSE等；
 
- V-BLAST分集阶数在L-K和L之间；
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-8b6a578b3c50458dab466ceda0c7eb48!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
V-BLAST算法示意图

 
以2 X 2 MIMO为例：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-a6ac6572bf2441e5b08ef636b1f6e39c!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
若  h1>h2,先解码 x1，否则先解码 x2.

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-6346a0a058cc4372be3d51a46ff7a05f!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
判决

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-eb032730f9af478895e20847f20f3392!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
V-BLAST 认为：既然我一次听不清所有人说话，那我就先听嗓门最大的那个人说话。

 
 
- 排序 (Ordering)：先用线性算法（如 ZF 或 MMSE）探测一下，看哪根天线的信号质量（信噪比）最好。
 
- 检测 (Detection)：先把这个最强的信号解调出来，做出判决（比如判定它是 '1'）。
 
- 重构与消除 (Cancellation)：既然我已经判定它是 '1' 了，我就根据信道 H 算出这个 '1' 对其他天线造成了多少干扰，然后从总接收信号 Y 里减去这个干扰。
 
- 循环：减去最强信号后，剩下的信号干扰变少了。再从剩下的里面找最强的，重复上述步骤。
 

 
 
- 优点：性价比高。性能比简单的 ZF/MMSE 好很多，复杂度又远低于 MLD。
 
- 
缺点：误差传播 (Error Propagation)。

 
 
- 如果在第一步（最强信号）判决错了，把它减掉时就会引入新的错误，导致后面所有的信号都解错。一步错，步步错。
 

 
 

 
 
- 你发现 A 的声音最大。你集中精力先把 A 的话听写下来。
 
- 然后你在脑子里把 A 的声音“屏蔽”掉（减去）。
 
- 这时候 B 和 C 的声音就清晰多了，你再听 B 的……
 

 

 
最大似然检测——MLD(Maximum Likelihood Detection)

 
- 目标函数是最小化
 
- ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-f56f451149c248ab8a08568225cb9ead!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
 
 为所有可能的发送信号，以2X2 MIMO、[QPSK调制为例，  有16种可能的情况。  为信道矩阵；  为随机产生的二进制序列经过QPSK调制后经过信道后接收端接收到的信号。

 
在高SNR下，MLD的BER渐进边界大致为

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-ca583f97ed354171b59c86b04bc9843f!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
原理：

 
 
- 接收端知道发送端可能发送的所有信号组合（比如 QPSK 调制，2根发射天线，一共就有 4^2=16种组合）。
 
- 接收机把这 16 种组合全部试一遍：假设发的是 A，经过信道 H后应该是多少？
 
- 把计算结果和实际收到的信号 Y 对比。
 
- 谁最像（欧氏距离最小），我就认为是发的谁。
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-f7762e47bf6c4213a23596a59f13d93f!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
 
- 优点：性能最强 (Optimal)。它是理论上的天花板，误码率最低。
 
- 
缺点：复杂度爆炸。

 
 
- 如果你用 64-QAM，4 根天线。组合数是 $64^4 = 16,777,216$ 种。
 
- 每接收一个符号，就要算 1600 万次距离。这在工程上几乎是不可实现的（除非用球形译码 Sphere Decoding 等优化算法）。
 

 
 

 

 
它是一个迭代的过程（洋葱剥皮）：

 
优缺点：

 
类比： 聚会上 A、B、C 同时在说话。

 

 
MLD 根本不讲道理，也不试图去解方程。它做的事情非常简单：

 
优缺点：