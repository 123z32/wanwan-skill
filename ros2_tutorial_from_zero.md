# 🤖 ROS2 从零开始入门教程

**作者**: 绾绾  
**日期**: 2026-03-18  
**适用**: ROS2 初学者，有编程基础

---

## 📖 目录

1. [ROS2 是什么？](#1-ros2-是什么)
2. [核心概念](#2-核心概念)
3. [通信机制](#3-通信机制)
4. [实际例子](#4-实际例子)
5. [你的代码包解析](#5-你的代码包解析)

---

## 1. ROS2 是什么？

### 1.1 简单理解

**ROS2 = 机器人的"操作系统" + "通信框架"**

但它不是真正的操作系统（像 Windows/Linux），而是：
- **运行在 Linux 之上**的软件框架
- **提供标准接口**让机器人各个部分能互相通信
- **提供工具**让开发机器人更容易

### 1.2 类比理解

**想象你在开一家餐厅** 🍽️

| 餐厅角色 | ROS2 对应 | 说明 |
|---------|----------|------|
| **厨师** | 传感器节点 | 采集数据（激光雷达、摄像头） |
| **服务员** | 通信系统 | 传递消息（话题、服务） |
| **经理** | 控制节点 | 做决策（导航、避障） |
| **菜谱** | 消息格式 | 标准化数据格式 |
| **厨房** | ROS2 系统 | 协调所有人工作 |

**没有 ROS2 时**:
```
厨师 → 大喊 → 服务员 → 跑步 → 经理
(每个部件都要自己写通信代码，累死！)
```

**有 ROS2 后**:
```
厨师 → 发布消息 → ROS2 → 订阅消息 → 经理
(标准化通信，专注业务逻辑)
```

---

## 2. 核心概念

### 2.1 Node (节点)

**定义**: 一个独立的功能模块

**比喻**: 餐厅里的**每个员工**

**例子**:
```
👨‍🍳 激光雷达节点 - 负责采集激光数据
👩‍🍳 IMU 节点 - 负责采集姿态数据
👨‍🍳 建图节点 - 负责构建地图
👩‍🍳 导航节点 - 负责路径规划
```

**代码示例**:
```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')  # 节点名字叫"my_node"
        self.get_logger().info('节点启动啦！')

def main():
    rclpy.init()
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()

if __name__ == '__main__':
    main()
```

**运行**:
```bash
# 启动节点
ros2 run my_package my_node

# 查看节点列表
ros2 node list
```

---

### 2.2 Topic (话题)

**定义**: 节点之间**单向广播**通信的渠道

**比喻**: 餐厅里的**广播系统** 📢

**特点**:
- **发布/订阅模式** (Publish/Subscribe)
- **单向传输** (发布者不知道谁在听)
- **多对多通信** (一个发布，多个订阅)

**例子**:
```
激光雷达节点 --发布--> /scan 话题 --订阅--> 建图节点
                              └--> 导航节点
                              └--> 避障节点
```

**常见话题**:
| 话题名 | 数据类型 | 用途 |
|--------|---------|------|
| `/scan` | LaserScan | 2D 激光雷达数据 |
| `/points_raw` | PointCloud2 | 3D 点云数据 |
| `/imu/data` | Imu | IMU 姿态数据 |
| `/odom` | Odometry | 里程计数据 |
| `/map` | OccupancyGrid | 栅格地图 |
| `/cmd_vel` | Twist | 速度指令 |

**代码示例**:
```python
# 发布激光数据的节点
class LaserPublisher(Node):
    def __init__(self):
        super().__init__('laser_pub')
        # 创建发布者，发布到/scan 话题
        self.publisher = self.create_publisher(LaserScan, '/scan', 10)
        
    def publish_scan(self):
        msg = LaserScan()
        msg.ranges = [1.5, 2.3, 1.8, ...]  # 激光数据
        self.publisher.publish(msg)

# 订阅激光数据的节点
class LaserSubscriber(Node):
    def __init__(self):
        super().__init__('laser_sub')
        # 创建订阅者，订阅/scan 话题
        self.subscription = self.create_subscription(
            LaserScan, 
            '/scan', 
            self.callback, 
            10
        )
    
    def callback(self, msg):
        self.get_logger().info(f'收到激光数据：{len(msg.ranges)} 个点')
```

**命令行操作**:
```bash
# 查看话题列表
ros2 topic list

# 查看话题类型
ros2 topic type /scan

# 查看话题数据
ros2 topic echo /scan

# 查看话题频率
ros2 topic hz /scan

# 手动发布消息
ros2 topic pub /scan sensor_msgs/msg/LaserScan "{ranges: [1.0, 2.0, 3.0]}"
```

---

### 2.3 Message (消息)

**定义**: 话题中传输的**数据格式**

**比喻**: 餐厅里的**标准单据** 📄

**常见消息类型**:

#### LaserScan (2D 激光扫描)
```yaml
header:
  stamp: {sec: 123, nanosec: 456}  # 时间戳
  frame_id: "laser_link"            # 坐标系
angle_min: -3.14                    # 最小角度 (-180°)
angle_max: 3.14                     # 最大角度 (+180°)
angle_increment: 0.017              # 角度增量 (1°)
ranges: [1.5, 2.3, 1.8, ...]        # 距离数据 (米)
```

#### PointCloud2 (3D 点云)
```yaml
header:
  stamp: {sec: 123, nanosec: 456}
  frame_id: "laser_link"
height: 1                           # 1=单线，>1=多线
width: 16384                        # 点数
fields:                             # 每个点的字段
  - name: x
    datatype: FLOAT32
  - name: y
    datatype: FLOAT32
  - name: z
    datatype: FLOAT32
data: [二进制数据]                   # 所有点的坐标
```

#### OccupancyGrid (栅格地图)
```yaml
header:
  stamp: {sec: 123, nanosec: 456}
  frame_id: "map"
info:
  resolution: 0.05      # 分辨率 (0.05 米/像素)
  width: 2000           # 地图宽度 (像素)
  height: 2000          # 地图高度 (像素)
  origin: ...           # 地图原点
data: [0, 0, 100, -1, ...]  # 栅格数据
                        # 0=空闲，100=障碍，-1=未知
```

---

### 2.4 Frame (坐标系)

**定义**: 描述物体位置的**参考系**

**比喻**: 地图上的**经纬度系统** 🌍

**常见坐标系**:

```
map (世界坐标系)
  ↓
odom (里程计坐标系)
  ↓
base_link (机器人基座)
  ↓
laser_link (激光雷达)
  ↓
camera_link (摄像头)
```

**每个坐标系的含义**:

| 坐标系 | 含义 | 谁发布的 |
|--------|------|---------|
| `map` | 固定世界坐标 | SLAM/AMCL |
| `odom` | 相对里程计坐标 | 里程计节点 |
| `base_link` | 机器人中心 | 机器人本身 |
| `laser_link` | 激光雷达位置 | 静态 TF |
| `camera_link` | 摄像头位置 | 静态 TF |

**为什么需要多个坐标系？**

想象你在房间里走路：
- **map**: 以房间角落为原点 (绝对位置)
- **odom**: 以你起点为原点 (相对位置)
- **base_link**: 以你的肚子为原点 (身体中心)
- **laser_link**: 以你的眼睛为原点 (传感器位置)

**TF 变换**:
```
map → odom: 机器人在世界中的位置
odom → base_link: 机器人的里程计
base_link → laser_link: 激光雷达安装位置
```

---

### 2.5 TF (坐标变换)

**定义**: 不同坐标系之间的**转换关系**

**比喻**: 不同语言之间的**翻译器** 🗣️

**为什么需要 TF？**

激光雷达说："障碍物在我前方 2 米"
导航节点问："障碍物在**地图**的哪个位置？"

**TF 负责翻译**:
```
激光坐标系：前方 2 米
    ↓ (TF 变换)
base_link 坐标系：机器人前方 2 米
    ↓ (TF 变换)
odom 坐标系：距离起点 5 米
    ↓ (TF 变换)
map 坐标系：世界坐标 (10, 20)
```

**TF 树结构**:
```
        map
         │
         ↓ (AMCL 发布)
        odom
         │
         ↓ (里程计/SLAM 发布)
    base_link
     ╱     ╲
    ↓       ↓
laser   camera
```

**检查 TF**:
```bash
# 查看 TF 树
ros2 run tf2_tools view_frames.py

# 查看 TF 监控
ros2 run tf2_ros tf2_monitor

# 监听 TF 变换
ros2 run tf2_ros tf2_echo map base_link
```

---

### 2.6 Package (功能包)

**定义**: ROS2 的**代码组织单元**

**比喻**: 餐厅里的**部门** 🏢

**典型结构**:
```
my_package/
├── package.xml          # 包的描述文件 (类似简历)
├── setup.py             # 安装配置
├── src/                 # 源代码
│   ├── my_node.py       # Python 节点
│   └── ...
├── launch/              # 启动文件
│   └── my_launch.py     # 一键启动
├── config/              # 配置文件
│   └── params.yaml      # 参数配置
└── resource/            # 资源文件
```

**package.xml 示例**:
```xml
<package format="3">
  <name>my_package</name>
  <version>1.0.0</version>
  <description>我的 ROS2 包</description>
  
  <depend>rclpy</depend>
  <depend>sensor_msgs</depend>
  <depend>geometry_msgs</depend>
</package>
```

---

### 2.7 Launch (启动文件)

**定义**: **一键启动多个节点**的配置文件

**比喻**: 餐厅的**开业流程** 🎬

**为什么需要 Launch？**

手动启动 10 个节点：
```bash
# 累死人的方式
ros2 run pkg node1
# 打开新终端
ros2 run pkg node2
# 打开新终端
ros2 run pkg node3
# ... 重复 10 次
```

**使用 Launch**:
```bash
# 一条命令搞定
ros2 launch pkg my_launch.py
```

**Launch 文件示例**:
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 启动激光雷达节点
        Node(
            package='lslidar_driver',
            executable='lslidar_node',
            name='laser_driver'
        ),
        
        # 启动建图节点
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer'
        ),
        
        # 启动导航节点
        Node(
            package='nav2_bringup',
            executable='nav2_node',
            name='nav2'
        )
    ])
```

---

## 3. 通信机制

### 3.1 三种通信方式

ROS2 有三种节点间通信方式：

| 方式 | 比喻 | 特点 | 例子 |
|------|------|------|------|
| **Topic** | 广播系统 | 单向，多对多 | 激光数据、IMU 数据 |
| **Service** | 打电话 | 双向，有回应 | 保存地图、重启服务 |
| **Action** | 快递 | 异步，可取消 | 导航到某点、机械臂抓取 |

---

### 3.2 Topic (话题通信)

**特点**:
- 发布/订阅模式
- 单向传输
- 实时数据流

**例子**: 激光雷达持续发布数据
```
激光节点 --发布--> /scan --订阅--> 建图节点
                           └--> 导航节点
                           └--> 避障节点
```

---

### 3.3 Service (服务通信)

**特点**:
- 请求/响应模式
- 双向通信 (有回应)
- 同步阻塞

**例子**: 保存地图服务
```python
# 客户端发起请求
ros2 service call /save_map cartographer_ros_msgs/srv/WriteState \
  "{filename: '/tmp/map.pbstream'}"

# 服务端处理并返回
响应：{success: true, message: "地图已保存"}
```

**常见服务**:
| 服务名 | 用途 |
|--------|------|
| `/save_map` | 保存地图 |
| `/finish_trajectory` | 结束建图 |
| `/set_pose` | 设置机器人位置 |

---

### 3.4 Action (动作通信)

**特点**:
- 异步执行
- 可中途取消
- 有进度反馈

**例子**: 导航到某点
```python
# 发送目标
action_client.send_goal(
    target_pose = (x=10, y=20, theta=0)
)

# 中途可以收到进度反馈
反馈：已走 50%
反馈：已走 80%
反馈：到达目标！

# 随时可以取消
action_client.cancel_goal()
```

---

## 4. 实际例子

### 4.1 激光雷达建图流程

让我们用你的代码包来理解完整流程：

```
┌─────────────────────────────────────────────────┐
│              物理世界                            │
│                                                 │
│    障碍物 ──── 2 米 ────→ [机器人]              │
│                                                 │
└─────────────────────────────────────────────────┘
                    ↓
              激光雷达发射激光
                    ↓
              激光反射回来
                    ↓
┌─────────────────────────────────────────────────┐
│           激光雷达硬件                           │
│   测量激光往返时间 → 计算距离                     │
│   生成 16 线 3D 点云数据                          │
└─────────────────────────────────────────────────┘
                    ↓
              发布原始数据
                    ↓
           话题：/cx/points_raw
                    ↓
┌─────────────────────────────────────────────────┐
│        single_lidar_dispose 节点                │
│   功能：从 16 线点云中提取单环 (第 8 线)            │
│   输入：/cx/points_raw (3D 点云)                │
│   输出：/cx/laserscan (2D 激光)                 │
└─────────────────────────────────────────────────┘
                    ↓
              发布 2D 激光数据
                    ↓
            话题：/cx/laserscan
                    ↓
         ┌────────┴────────┐
         ↓                 ↓
┌─────────────────┐ ┌─────────────────┐
│ Cartographer    │ │   RViz2         │
│ 建图节点        │ │   显示节点      │
│                 │ │                 │
│ 订阅：/scan     │ │ 订阅：/scan     │
│ 订阅：/imu      │ │ 显示：激光线    │
│                 │ │                 │
│ 内部处理：      │ │                 │
│ - 扫描匹配     │ │                 │
│ - 位姿估计     │ │                 │
│ - 子地图构建   │ │                 │
└─────────────────┘ └─────────────────┘
         ↓
         │ 内部地图数据
         ↓
┌─────────────────┐
│ occupancy_grid  │
│ 节点            │
│                 │
│ 功能：将内部    │
│ 地图转换为      │
│ 标准格式        │
└─────────────────┘
         ↓
         │ 发布/map 话题
         ↓
    ┌────┴────┐
    ↓         ↓
  RViz2     Nav2
  显示地图  导航规划
```

---

### 4.2 一步一步解析

#### 步骤 1: 激光雷达采集

```bash
# 启动激光雷达驱动
ros2 launch lslidar_driver lslidar_cx_launch.py
```

**发生了什么**:
1. 激光雷达硬件开始工作
2. 发射激光束
3. 接收反射光
4. 计算距离
5. 生成 3D 点云
6. 发布到 `/cx/points_raw` 话题

**数据格式**:
```yaml
/cx/points_raw:
  header:
    frame_id: "laser_link"
  height: 16        # 16 线
  width: 1024       # 每线 1024 个点
  fields: [x, y, z, intensity, ring]
```

---

#### 步骤 2: 提取单环激光

```bash
# 启动单环处理节点
ros2 run un_ld_ws single_lidar_dispose
```

**发生了什么**:
1. 订阅 `/cx/points_raw` (3D 点云)
2. 提取第 8 线的点
3. 转换成 2D LaserScan 格式
4. 发布到 `/cx/laserscan`

**代码核心逻辑**:
```python
def point_cloud_callback(self, msg):
    # 1. 遍历所有点
    for p in points:
        # 2. 只保留第 8 线的点
        if p.ring == 8:
            # 3. 计算极坐标 (距离，角度)
            distance = sqrt(p.x² + p.y²)
            angle = atan2(p.y, p.x)
            laser_points.append((angle, distance))
    
    # 4. 发布 LaserScan 消息
    scan_msg.ranges = distances
    self.laserscan_pub.publish(scan_msg)
```

---

#### 步骤 3: Cartographer 建图

```bash
# 启动建图节点
ros2 launch cartographer_config cartographer_2d_launch.py
```

**发生了什么**:
1. 订阅 `/cx/laserscan` (2D 激光)
2. 订阅 `/imu/data` (IMU 姿态)
3. 进行扫描匹配
4. 估计机器人位姿
5. 构建子地图
6. 优化轨迹

**内部流程**:
```
激光数据 → 扫描匹配 → 位姿估计 → 子地图
   ↓                        ↓
IMU 数据 → 位姿预测 ────────→ 轨迹优化
```

---

#### 步骤 4: 发布地图

```bash
# occupancy_grid 节点自动启动 (在 launch 文件里)
```

**发生了什么**:
1. 订阅 Cartographer 的内部地图
2. 融合所有子地图
3. 转换成 OccupancyGrid 格式
4. 发布到 `/map` 话题

**输出数据**:
```yaml
/map:
  header:
    frame_id: "map"
  info:
    resolution: 0.05    # 5 厘米/像素
    width: 2000         # 100 米宽
    height: 2000        # 100 米高
  data: [0, 0, 100, -1, ...]
        # 0=空闲区域
        # 100=障碍物
        # -1=未知区域
```

---

#### 步骤 5: 显示地图

```bash
# 启动 RViz2
ros2 run rviz2 rviz2
```

**在 RViz2 中添加**:
1. **LaserScan** 显示 → 看到激光扫描线
2. **Map** 显示 → 看到构建的地图
3. **TF** 显示 → 看到坐标变换树

---

## 5. 你的代码包解析

### 5.1 完整架构

```
ros2_code_ws/
│
├── src/
│   │
│   ├── Lslidar_ROS2_driver/     # 激光雷达驱动包
│   │   └── lslidar_driver/
│   │       ├── launch/           # 启动文件
│   │       │   └── lslidar_cx_launch.py
│   │       └── src/              # C++ 驱动代码
│   │
│   ├── un_ld_ws/                 # 激光处理包 ⭐
│   │   └── un_ld_ws/
│   │       ├── single_lidar_dispose.py    # 单环提取
│   │       ├── b2_command_trigger.py      # 命令触发
│   │       └── b2_keyboard_control.py     # 键盘控制
│   │
│   ├── cartographer_config/      # 建图配置包
│   │   ├── launch/
│   │   │   └── cartographer_2d_launch.py
│   │   ├── cartographer_2d.lua   # 建图参数
│   │   └── package.xml
│   │
│   ├── b2_bringup/               # 系统启动包
│   │   └── launch/
│   │       └── b2_bringup.launch.py
│   │
│   └── un_omnirange_ws/          # 全向雷达包
│       └── un_omnirange_ws/
│           └── b2_nav2_control_old.py
│
└── map_factory/                  # 地图工厂
    └── 保存的地图文件
```

---

### 5.2 每个包的作用

#### Lslidar_ROS2_driver
**作用**: 驱动速腾聚创 C16 激光雷达
**发布**: `/cx/points_raw` (3D 点云)
**类似**: 打印机的驱动程序

---

#### un_ld_ws
**作用**: 处理激光雷达数据
**核心节点**: `single_lidar_dispose.py`
**输入**: 3D 点云 (16 线)
**输出**: 2D LaserScan (单环)
**类似**: 图片压缩软件 (3D→2D)

---

#### cartographer_config
**作用**: SLAM 建图
**核心**: Cartographer 算法
**输入**: 2D 激光 + IMU
**输出**: 内部地图数据
**类似**: 摄影师拍照 + 拼图

---

#### occupancy_grid (节点)
**作用**: 发布标准地图
**输入**: Cartographer 内部数据
**输出**: `/map` 话题
**类似**: 冲印照片 (数字→实体)

---

#### b2_bringup
**作用**: 一键启动整个系统
**类似**: 开机启动脚本

---

### 5.3 完整启动命令解析

```bash
# 完整启动流程
source /opt/ros/humble/setup.bash           # 1. 设置 ROS2 环境
source /root/ws/ros2_b2w/unitree_ros2/install/setup.bash  # 2. 设置 Unitree 环境
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp # 3. 设置通信中间件
source ~/ws/ros2_code_ws/text_ws/install/setup.bash  # 4. 设置工作空间

# 启动激光雷达
ros2 launch lslidar_driver lslidar_cx_launch.py

# 启动单环处理
ros2 run un_ld_ws single_lidar_dispose

# 启动建图
ros2 launch cartographer_config cartographer_2d_launch.py

# 启动 TF 变换
ros2 run tf2_ros static_transform_publisher \
  --frame-id base_link \
  --child-frame-id laser_link
```

---

## 6. 关键概念总结

### 6.1 一句话理解

| 概念 | 一句话理解 |
|------|-----------|
| **Node** | 独立的功能模块 |
| **Topic** | 数据广播渠道 |
| **Message** | 数据格式标准 |
| **Frame** | 位置参考系 |
| **TF** | 坐标系翻译器 |
| **Package** | 代码组织单元 |
| **Launch** | 一键启动脚本 |

---

### 6.2 数据流总结

```
物理世界
   ↓
激光雷达硬件
   ↓
3D 点云 (/cx/points_raw)
   ↓
single_lidar_dispose 节点
   ↓
2D 激光 (/cx/laserscan)
   ↓
Cartographer 节点
   ↓
内部地图数据
   ↓
occupancy_grid 节点
   ↓
标准地图 (/map)
   ↓
RViz2 显示 / Nav2 导航
```

---

## 7. 常用命令速查

```bash
# 节点管理
ros2 node list                    # 列出所有节点
ros2 node info /node_name         # 查看节点信息

# 话题管理
ros2 topic list                   # 列出所有话题
ros2 topic echo /topic_name       # 查看话题数据
ros2 topic hz /topic_name         # 查看话题频率
ros2 topic type /topic_name       # 查看话题类型

# TF 管理
ros2 run tf2_tools view_frames.py # 查看 TF 树
ros2 run tf2_ros tf2_monitor      # TF 监控

# 服务管理
ros2 service list                 # 列出所有服务
ros2 service call /srv_name ...   # 调用服务

# 启动管理
ros2 launch pkg launch_file.py    # 启动文件

# 包管理
ros2 pkg list                     # 列出所有包
ros2 pkg prefix pkg_name          # 查看包路径
```

---

## 8. 学习路线建议

### 第 1 周：基础概念
- ✅ 理解 Node、Topic、Message
- ✅ 学会用命令行查看节点和话题
- ✅ 编写简单的发布/订阅节点

### 第 2 周：TF 和坐标
- ✅ 理解坐标系概念
- ✅ 学会用 TF 工具
- ✅ 发布静态 TF 变换

### 第 3 周：实际项目
- ✅ 运行你的激光雷达包
- ✅ 理解数据流
- ✅ 调试建图问题

### 第 4 周：深入理解
- ✅ 修改参数优化建图
- ✅ 添加自定义功能
- ✅ 集成 Nav2 导航

---

*教程完成时间：2026-03-18*  
*作者：绾绾*  
*有问题随时问我！* 😊
