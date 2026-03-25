# 浅析IQ调制和解调(正交调制)

> 来源: OneNote > 通信 > 1
> 修改: 2025-12-01T13:39:23Z

浅析IQ调制和解调(正交调制)
 
 
 
 
 

 
 
IQ调制

 
IQ调制,英文名称为In-phase and Quadrature Modulation，又称为[正交调制。这种调制方式是一种高效的信号调制技术，广泛应用于无线通信、雷达、卫星通信等领域。IQ调制的本质是通过两路正交载波信号（余弦和负正弦）同时传输两路调制信号，从而实现并行信号传输。

 
IQ调制的原理

 
IQ 调制的过程可以表示为：

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-2683c745d1104e18995846ea77c62857!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
其中：

 
- x(t)和y(t)是调制信号（I 路和 Q 路信号）。
 
- cos⁡(ωct)和−sin⁡(ωct)是正交载波信号。
 
- s(t)是调制后的信号。
 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-3c894963de0e4efbbe04ae5cdf41b512!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
IQ调制利用两路正交载波信号的正交性，将两路调制信号叠加到同一频段内，从而实现频谱效率的提升。

 
二、IQ解调

 
IQ解调是从调制信号s(t)中恢复出原始的I路信号x(t)和Q路信号y(t)。解调过程包括：

 

 
与载波信号相乘：

 
将调制信号s(t)分别与两路正交载波信号cos⁡(ωct)和sin⁡(ωct)相乘，即s(t)⋅cos⁡(ωct)和s(t)⋅sin⁡(ωct)。

 

 
低通滤波：

 
通过[低通滤波器滤除高频成分，保留调制信号的基带成分，从而恢复出原始的I路和Q路信号。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-20f0e823ac5649a1841b6be856472eb6!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
解调过程的计算公式如下：

 
低通滤波的作用，通过低通滤波器，可以滤除上述公式中中高频成分cos⁡(2ωct)和sin⁡(2ωct)。

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-2cb25452cfca453ea053c7c639dde75f!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 

 
三、IQ调制和解调的Matlab仿真

 
IQ调制和解调的Matlab仿真功能步骤：

 
- 设置参数（采样率、时间、载频、基带频率）。
 
- 生成基带信号（I路和Q路）。
 
- 进行IQ调制（乘以正交载波并相加）。
 
- 绘制调制信号（I和Q）和已调信号。
 
- 解调：用正交载波下变频，然后低通滤波恢复基带信号。
 
- 绘制原始基带信号和解调恢复信号的对比图（I路和Q路分开）。
 

 

 
%% IQ调制解调MATLAB仿真￼clear; clc; close all;￼%% 1. 参数设置￼Fs = 5000; % 采样率 (Hz)￼t = 0:1/Fs:1; % 时间向量￼fc = 1000; % 载波频率 (Hz) - 对应 ω_c = 2π*fc￼% 生成调制信号 I路和Q路￼f_msg = 10; % 基带信号频率￼x_t = 0.8*cos(2*pi*f_msg*t); % I路信号（实部）￼y_t = 0.5*sin(2*pi*1.5*f_msg*t); % Q路信号（虚部）注意正交性！￼%% 2. IQ调制￼carrier_cos = cos(2*pi*fc*t); % 载波 cos(ω_c t)￼carrier_sin = -sin(2*pi*fc*t); % 载波 -sin(ω_c t) 注意负号！￼% 调制过程￼s_t = x_t .* carrier_cos + y_t .* carrier_sin; % s(t) = x(t)cos(ω_ct) - y(t)sin(ω_ct)￼%% 3. 调制可视化￼figure;￼subplot(2,1,1);￼plot(t, x_t, 'b', t, y_t, 'r');￼legend('I路信号 x(t)', 'Q路信号 y(t)');￼title('调制信号');￼xlabel('时间 (s)'); grid on;￼subplot(2,1,2);￼plot(t, s_t, 'g');￼title('已调信号 s(t)');￼xlabel('时间 (s)'); grid on;￼%% 4. 解调过程￼% 本地振荡器（理想[相干解调）￼local_cos = cos(2*pi*fc*t);￼local_sin = -sin(2*pi*fc*t);￼% 解调乘法器￼demod_I = s_t .* local_cos; % s(t)*cos(ω_c t)￼demod_Q = s_t .* local_sin; % -s(t)*sin(ω_c t)￼% 低通滤波器设计（￼lpFilt = designfilt('lowpassfir', 'CutoffFrequency', 2*fc/Fs, ...￼'FilterOrder', 50, 'SampleRate', Fs);￼% 滤波恢复基带信号￼x_recovered = 2 * filtfilt(lpFilt.Coefficients, 1, demod_I); % I路输出￼y_recovered = 2 * filtfilt(lpFilt.Coefficients, 1, demod_Q); % Q路输出￼%% 5. 解调结果可视化￼figure;￼subplot(2,1,1);￼plot(t, x_t, 'b', t, x_recovered, 'r--');￼legend('原始I路信号', '解调恢复信号');￼title('I路信号恢复对比'); grid on;￼subplot(2,1,2);￼plot(t, y_t, 'b', t, y_recovered, 'r--');￼legend('原始Q路信号', '解调恢复信号');￼title('Q路信号恢复对比'); grid on;

 

 
仿真结果验证

 
蓝色(I路)低频振幅大，红色(Q路)高频振幅小

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-1ac6569fc2e24f7bbc8bacae42f664ee!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 
红虚线(Q路恢复)与蓝实线(原始Q路)高度重合

 ![图片](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-085fa0d8ec8b46d6af4bd7d5aa339bf5!1-9E53C6D99C1E5AD1!sdee902dab68e44faa500bc13467293df/$value)
 

 来自 <[https://zhuanlan.zhihu.com/p/1935670611394425832> 
 

 

 

 

 

 

 

 

 来自 <[https://zhuanlan.zhihu.com/p/1935670611394425832>