# Boost升压型

> 来源: OneNote > 电源类 > DC-DC开关电源 拓扑结构
> 修改: 2025-10-31T17:12:40Z

Boost升压型
 
 
 
 
 

 
 
Boost升压型电路拓扑，有时又称为step-up电路，其典型的电路结构如下图4所示：

 
　　

 [ ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-456fd57130884c218e8d97afb65b20c5!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value) 
　　同样地，根据Buck电路的分析方式，Boost电路的工作原理为：

 
　　

 [ ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-97a3a41e697e4f9f8a1e7070a2083b8e!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value) 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-6c0f798c3161446ab9bcd284e08608c1!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-b0dae5a8991342b4b13e5be74c637c7b!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value)
 
关键参数与设计要点

 
- 占空比（D）
 
- 理论上 D 接近 1 时，Vout可无限大，但实际中受开关管导通电阻、二极管压降、电感内阻影响，D 超过 0.85 后效率会急剧下降，因此 Boost 不适合 “输入电压远低于输出电压” 的极端场景（如 1.5V→24V，需多级升压）。
 
- 电感选型
 
- 电感量 L 过小：电流波动大，纹波增加，甚至进入断续模式（DCM）；
 
- 电感量过大：响应速度慢，体积大。
 
- 核心参数：饱和电流IRMS>=最大峰值电流（需计算，通常为平均电流的 1.5~2 倍），避免磁饱和（饱和后电感量骤降，失去储能能力）。
 
- ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-340f709a577b4b40a4781d318bd71e01!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value)
 
 
工作模式（CCM vs DCM）

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-ce94358ff9de4e208beb40a4ae69983d!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value)
 

 

 [ ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-456fd57130884c218e8d97afb65b20c5!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value) [![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-97a3a41e697e4f9f8a1e7070a2083b8e!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value)