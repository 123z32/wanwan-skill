# BUCK减压型

> 来源: OneNote > 电源类 > DC-DC开关电源 拓扑结构
> 修改: 2025-10-31T16:56:43Z

BUCK减压型
 
 
 
 
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-dd4e21e7853440429cb3cd736ef6597a!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value)
 
图中器件T为  N-mos管

 
当PWM驱动高电平使得NMOS管T导通的时候，忽略MOS管的导通压降，等效如图2，电感电流呈线性上升，MOS导通时电感正向伏秒为：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-83ccb87cf0a7461a9b13b691500fd702!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value)
 
当PWM驱动低电平的时候，MOS管截止，电感电流不能突变，经过续流二极管形成回路（忽略二极管电压），给输出负载供电，此时电感电流下降，如下图3所示，MOS截止时电感反向伏秒为：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-aedb90e3583d4f409027dc382059ef1d!1-9E53C6D99C1E5AD1!s0b840cbde1484b0fb11d20b3092261e9/$value)
 
什么是电感的伏秒平衡呐？

 
处于稳定状态的电感，开关导通时间(电流上升段)的伏秒数须与开关关断(电流下降段)时的伏秒数在数值上相等，尽管两者符号相反。这也表示，绘出电感电压对时间的曲线，导通时段曲线的面积必须等于关断时段曲线的面积。