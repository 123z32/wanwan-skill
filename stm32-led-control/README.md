# STM32F407VGT6 SkyStar LED 控制项目

## 📋 项目说明

控制 SkyStar 星空板板载 LED 的示例程序，实现 LED 闪烁效果。

## 🔧 硬件信息

- **开发板**: LCKFB LSPI SkyStar STM32F407VGT6 PRO
- **MCU**: STM32F407VGT6 (ARM Cortex-M4F, 168MHz)
- **LED 连接**:
  - LED0: PF9 (低电平点亮)
  - LED1: PF10 (低电平点亮)

## 📁 文件结构

```
stm32-led-control/
├── main.c          # 主程序 + LED 控制函数
├── main.h          # 头文件
├── README.md       # 说明文档
└── STM32F407VGTx_FLASH.ld  # 链接脚本 (需从 CubeMX 生成)
```

## 🛠️ 编译方法

### 方法 1: STM32CubeIDE

1. 打开 STM32CubeIDE
2. 新建 STM32 项目，选择 STM32F407VGTx
3. 配置时钟和 GPIO（参考下方 CubeMX 配置）
4. 将 `main.c` 代码复制到生成的 `main.c` 中
5. 编译并烧录

### 方法 2: Makefile (ARM GCC)

```bash
# 安装工具链
sudo apt install gcc-arm-none-eabi

# 编译
make

# 烧录 (使用 ST-Link)
st-flash write build/main.bin 0x8000000
```

### 方法 3: PlatformIO

```bash
# 安装 PlatformIO
pip install platformio

# 创建项目
pio init --board nucleo_f407vg

# 复制 main.c 到 src/ 目录
# 编译
pio run

# 烧录
pio run --target upload
```

## ⚙️ STM32CubeMX 配置

如需使用 STM32CubeMX 生成初始化代码，按以下步骤配置：

### 1. Pinout 配置
- **PF9**: GPIO_Output (LED0)
- **PF10**: GPIO_Output (LED1)
- **SYS**: Debug → Serial Wire (SWD)

### 2. Clock 配置
- HSE: Crystal/Ceramic Resonator
- PLL Source: HSE
- PLL M: 25
- PLL N: 336
- PLL P: 2
- System Clock: 168 MHz

### 3. Project Manager
- Toolchain: Makefile 或 STM32CubeIDE
- 生成代码后，将 `main.c` 中的函数复制到生成的文件中

## 🔌 烧录方法

### ST-Link Utility (Windows)
1. 连接 ST-Link 到开发板
2. 打开 STM32CubeProgrammer
3. 选择 ST-Link 接口
4. 加载 `.hex` 或 `.bin` 文件
5. 点击 "Download"

### OpenOCD (Linux/Mac)
```bash
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg -c "program main.elf verify reset exit"
```

### PyOCD
```bash
pyocd flash -t stm32f407vg main.elf
```

## 🎯 功能说明

程序运行后：
- LED0 和 LED1 交替闪烁
- 闪烁间隔：500ms
- 可通过修改 `HAL_Delay_ms()` 参数调整闪烁速度

## 📝 修改 LED 引脚

如果你的开发板 LED 引脚不同，修改 `main.c` 中的定义：

```c
#define LED0_PIN    GPIO_PIN_9   /* 修改为你的引脚 */
#define LED0_PORT   GPIOF        /* 修改为你的端口 */
```

常见引脚：
- LED: PF9/PF10 (SkyStar)
- LED: PG13/PG14 (NUCLEO-F407)
- LED: PD12/PD13/PD14/PD15 (Discovery)

## 🐛 常见问题

### Q: LED 不亮
**A**: 检查以下几点：
1. 确认 LED 引脚是否正确
2. 确认 LED 是低电平点亮还是高电平点亮
3. 检查 GPIO 时钟是否使能
4. 用万用表测量引脚电压

### Q: 编译报错
**A**: 确保：
1. 已安装正确的工具链
2. 链接脚本与 MCU 型号匹配
3. HAL 库版本兼容

### Q: 烧录失败
**A**: 检查：
1. ST-Link 驱动是否安装
2. 开发板供电是否正常
3. SWD 接口连接是否可靠

## 📚 参考资料

- [STM32F407 参考手册](https://www.st.com/resource/en/reference_manual/rm0090-stm32f40541542543546547-and-stm32f407417-advanced-armbased-32bit-mcus-stmicroelectronics.pdf)
- [STM32 HAL 库文档](https://www.st.com/resource/en/user_manual/um1725-description-of-stm32f4-hal-and-lowlayer-drivers-stmicroelectronics.pdf)
- [SkyStar 星空板资料](https://github.com/12345678/SkyStar)

---

*最后更新：2026-04-07*
*作者：绾绾*
