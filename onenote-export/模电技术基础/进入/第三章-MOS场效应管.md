# 第三章-MOS场效应管

> 来源: OneNote > 模电技术基础 > 进入
> 修改: 2024-06-21T01:54:43Z

第三章-MOS场效应管
 
 
 
 
 

 
第三章——MOS场效应管

 
[一.场效应管的分类：

 
[二.MOSFET的主要参数

 
[三.MOSFET放大电路的分析与计算

 
[四.各种放大器件电路性能比较

 

 

 
一.场效应管的分类：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-19413e5fb29d47cf8b2d85726c49a9d9!1-9E53C6D99C1E5AD1!205/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-de8ba5564b094ac1be01fff40ff1c640!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
**耗尽型：**场效应管没有加偏置电压时，就有导电沟道存在。

 
**增强型：**场效应管没有加偏置电压时，没有导电沟道。

 

 
结型场效应管（rbe可做到10的15次方)

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-46371c71a8444e12a6a60a7498f0d7c1!1-9E53C6D99C1E5AD1!205/$value)
 
栅极g 漏极d 源极s

 
漏极与源极之间的非耗尽层区域称为导电沟道。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-2aacdc05a23c4bbcb78d3ec04d2fe421!1-9E53C6D99C1E5AD1!205/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-7b9c5b47e68041f2b25043c0899186ff!1-9E53C6D99C1E5AD1!205/$value)
 

 

 

 

 

 
绝缘栅型场效应管（rbe可做到10的19次方)

 
MOS管的四种类型为：N沟道增强型管，N沟道耗尽型管，P*沟道增强型管，P沟道耗尽型管。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-3a8b67ee56f04dac921d7f201b8670a0!1-9E53C6D99C1E5AD1!205/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-62272d293a3546329dbda12c1232790b!1-9E53C6D99C1E5AD1!205/$value)
 
1.N沟道增强型MOSFET

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-0f1f70ef42374b33879acc98f42f304a!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
 

 
工作原理：

 
（1）vGS对沟道的控制作用：

 
当vGS≤0时：无导电沟道，d、s间加电压时，也无电流产生。

 
当0<vGS <VT 时：产生电场，但未形成导电沟道（感生沟道），d、s间加电压后，没有电流产生。

 
当vGS≥VT 时：在电场作用下产生导电沟道，d、s间加电压后，将有电流产生。

 
vGS越大，导电沟道越厚，其中VT 称为开启电压。

 
（2）vDS对沟道的控制作用：当vGS一定（vGS >VT ）时，vDS变大↑ → 使iD变大↑ → 从而使沟道电位梯度升高 → 靠近漏极d处的电位升高 → 电场强度减小 → 沟道变薄，整个沟道呈楔形分布。当vDS增加到使vGD=VT 时，在紧靠漏极处出现预夹断。在预夹断处：vGD = vGS - vDS = VT，预夹断后，vDS↑ → 夹断区延长 → 沟道电阻↑ → iD基本不变。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-ed2bc2b3c0ab4d928dda8a536b4966d4!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
**☆☆注：**若vDS和vGS同时作用时，假设vDS一定，vGS变化时，给定一个vGS ，就有一条不同的 iD – vDS 曲线。

 
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-157e25e645e348e4b9c9d97118c6d947!1-9E53C6D99C1E5AD1!205/$value)
 
**① 截止区：**当vGS＜VT时，导电沟道尚未形成，iD＝0，为截止工作状态。

 
② 可变电阻区：vDS≤（vGS－VT）时，rdso是一个受vGS控制的可变电阻。

 
③ 饱和区：vGS >VT ，且vDS≥（vGS－VT）

 
 

 
2.N沟道耗尽型MOSFET

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-4af9ec7092be45268e307f4eba6c31ec!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
二氧化硅绝缘层中掺有大量的正离子，可以在正或负的栅源电压下工作，而且基本上无栅流。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-3860c617baee4d3c88c53af7422287cd!1-9E53C6D99C1E5AD1!205/$value)
 
 

 
 

 
3.P沟道MOSFET

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-0ccee7488961444b8c01546c383047cf!1-9E53C6D99C1E5AD1!205/$value)
 
二.MOSFET的主要参数

 
直流参数：

 
（1）开启电压VT （增强型参数）

 
（2）夹断电压VP （耗尽型参数）

 
（3）饱和漏电流IDSS （耗尽型参数）

 
（4）直流输入电阻RGS （109Ω～1015Ω ）

 
**交流参数：**输出电阻rds、低频互导gm

 
**极限参数：**最大漏极电流IDM、最大耗散功率PDM、最大漏源电压V（BR）DS、最大栅源电压V（BR）GS

 
 

 
三.MOSFET放大电路的分析与计算

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-2b814cf626fb433dbc92b0ccdad1e376!1-9E53C6D99C1E5AD1!205/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-3baf67418a9c4db8825e8e54b56b5c28!1-9E53C6D99C1E5AD1!205/$value)
 
计算步骤：

 
（1）直流偏置及静态工作点的计算

 
（2）图解分析

 
（3）小信号模型分析

 
 

 
四.各种放大器件电路性能比较

 
mos 管利用栅源之间的电压 vgs 控制漏极电流，BJT利用基射极间的电压 vbe 控制集电极的电流 ic。但在放大区，mos管的 id 与 vgs 之间是平方律关系，而 BJT 的 ic 与 vbe 之间是指数关系，显然，指数关系更为敏感。故称 mos 管为电压控制器件，BJT 为电流控制器件。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-b42dba2b0c6e487094010c2f53c6996c!1-9E53C6D99C1E5AD1!205/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-469d6592dc604794a08aa89b45773b35!1-9E53C6D99C1E5AD1!205/$value)
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-b1d156a013954218a739e51bcbc12f3d!1-9E53C6D99C1E5AD1!205/$value)
 

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-f311d186d3934859ac57f0afc8ac6be4!1-9E53C6D99C1E5AD1!205/$value)
 

 
场效应管放大电路的三种接法

 
 共源放大电路、共漏放大电路和共栅放大电路

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-afa08be355dc4cbe8ba25a9e8880bf81!1-9E53C6D99C1E5AD1!205/$value)