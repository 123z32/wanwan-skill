# 🐛 ROS2 建图失败问题分析报告

**分析时间**: 2026-03-18 02:36 UTC  
**问题**: 只有激光雷达点图，没有地图生成  
**分析者**: 绾绾

---

## 🔍 问题诊断

### 症状
- ✅ 激光雷达点云正常显示
- ❌ 没有地图生成
- ❌ Cartographer 没有构建轨迹

---

## 🚨 发现的 5 个关键问题

### 问题 1: Cartographer 配置话题不匹配 ⚠️⚠️⚠️

**启动文件配置**:
```python
remappings=[
    ('scan', '/cx/laserscan'),    # 期望 2D 激光话题
    ('imu', '/imu/data')          # 期望 IMU 话题
]
```

**实际发布话题**:
- `single_lidar_dispose.py` 发布：`/cx/laserscan` ✅ (匹配)
- **但是**: 需要确认节点是否真的在运行并发布数据

**检查方法**:
```bash
# 查看话题列表
ros2 topic list | grep laser

# 查看话题内容
ros2 topic echo /cx/laserscan --once

# 查看话题频率
ros2 topic hz /cx/laserscan
```

---

### 问题 2: TF 坐标变换缺失 ⚠️⚠️⚠️

**Cartographer 需要的 TF**:
- `map` → `odom` → `base_link` → `laser_link`

**Lua 配置**:
```lua
tracking_frame = "base_link"
published_frame = "base_link"
odom_frame = "odom"
map_frame = "map"
```

**问题**: 
- README 中提到需要启动 TF 节点，但实际可能没启动
- 没有看到 `tf_publisher_node` 或 `tf_listener_node` 的运行

**检查方法**:
```bash
# 查看 TF 树
ros2 run tf2_tools view_frames.py
evince frames.pdf

# 或者
ros2 run tf2_ros tf2_monitor
```

---

### 问题 3: Cartographer 配置参数问题 ⚠️

**Lua 配置问题**:
```lua
num_laser_scans = 1        -- ✅ 正确，使用 2D 激光
num_point_clouds = 0       -- ✅ 正确，不使用 3D 点云
use_odometry = false       -- ⚠️ 可能需要设为 true
use_nav_sat = false        -- ✅ 正确，无 GPS
```

**建议修改**:
```lua
use_odometry = true  -- 如果有里程计数据
```

---

### 问题 4: 话题类型不匹配 ⚠️

**Cartographer 期望**:
- `/scan`: `sensor_msgs/msg/LaserScan`
- `/imu`: `sensor_msgs/msg/Imu`

**实际发布**:
- `/cx/laserscan`: `sensor_msgs/msg/LaserScan` ✅

**但是需要确认**:
- IMU 话题是否存在：`/imu/data`
- IMU 数据类型是否正确

**检查方法**:
```bash
# 检查 IMU 话题
ros2 topic list | grep imu
ros2 topic echo /imu/data --once
```

---

### 问题 5: 节点启动顺序问题 ⚠️

**正确启动顺序**:
1. 启动激光雷达驱动
2. 启动单环处理节点
3. **启动 TF 变换节点** ← 可能缺失
4. 启动 Cartographer 建图
5. 启动 occupancy_grid 节点

**当前可能缺失**:
- TF 变换节点没启动
- occupancy_grid 节点没启动

---

## ✅ 解决方案

### 步骤 1: 检查所有话题

```bash
# 1. 列出所有话题
ros2 topic list

# 2. 关键话题检查
ros2 topic echo /cx/points_raw --once        # 原始 3D 点云
ros2 topic echo /cx/laserscan --once         # 2D 激光扫描
ros2 topic echo /imu/data --once             # IMU 数据

# 3. 检查话题频率
ros2 topic hz /cx/laserscan
ros2 topic hz /imu/data
```

**期望输出**:
- `/cx/points_raw`: 10Hz 3D 点云
- `/cx/laserscan`: 10Hz LaserScan
- `/imu/data`: 50-100Hz IMU

---

### 步骤 2: 检查 TF 变换

```bash
# 1. 查看 TF 树
ros2 run tf2_tools view_frames.py

# 2. 检查 TF 监控
ros2 run tf2_ros tf2_monitor

# 3. 手动发布静态 TF（临时测试）
ros2 run tf2_ros static_transform_publisher \
  --x 0 --y 0 --z 0 \
  --roll 0 --pitch 0 --yaw 0 \
  base_link laser_link
```

**期望的 TF 树**:
```
map → odom → base_link → laser_link
```

---

### 步骤 3: 完整启动流程（修正版）

```bash
# ========== 环境准备 ==========
source /opt/ros/humble/setup.bash
source /root/ws/ros2_b2w/unitree_ros2/install/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
source ~/ws/ros2_code_ws/text_ws/install/setup.bash

# ========== 步骤 1: 启动激光雷达 ==========
# 在终端 1 运行
ros2 launch lslidar_driver lslidar_cx_launch.py

# ========== 步骤 2: 启动单环处理 ==========
# 在终端 2 运行
ros2 run un_ld_ws single_lidar_dispose

# ========== 步骤 3: 启动 TF 变换（关键！） ==========
# 在终端 3 运行
ros2 run tf2_ros static_transform_publisher \
  --frame-id base_link \
  --child-frame-id laser_link \
  --x 0 --y 0 --z 0 \
  --roll 0 --pitch 0 --yaw 0

# 或者运行完整的 TF 节点（如果有）
# ros2 run tf tf_publisher_node

# ========== 步骤 4: 启动 Cartographer ==========
# 在终端 4 运行
ros2 launch cartographer_config cartographer_2d_launch.py

# ========== 步骤 5: 验证 ==========
# 在新终端运行
ros2 topic list | grep map
ros2 topic echo /map --once
ros2 run rviz2 rviz2
```

---

### 步骤 4: 在 RViz2 中验证

```bash
# 启动 RViz2
ros2 run rviz2 rviz2
```

**添加显示项**:
1. **LaserScan** - Topic: `/cx/laserscan` (验证激光数据)
2. **Map** - Topic: `/map` (验证地图生成)
3. **TF** - 显示坐标变换
4. **PointCloud2** - Topic: `/cx/points_raw` (验证原始点云)

---

### 步骤 5: 诊断 Cartographer 状态

```bash
# 1. 查看 Cartographer 节点状态
ros2 node list

# 2. 查看 Cartographer 参数
ros2 param dump /cartographer_node

# 3. 查看服务
ros2 service list | grep cartographer

# 4. 获取轨迹状态
ros2 service call /trajectory_query cartographer_ros_msgs/srv/TrajectoryQuery \
  "{trajectory_id: 0}"
```

---

## 🔧 常见问题快速修复

### 问题 A: 没有 `/cx/laserscan` 话题

**原因**: `single_lidar_dispose.py` 节点没运行

**解决**:
```bash
# 启动节点
ros2 run un_ld_ws single_lidar_dispose

# 或者检查是否报错
ros2 run un_ld_ws single_lidar_dispose --ros-args --log-level debug
```

---

### 问题 B: 没有 TF 变换

**原因**: TF 发布节点没启动

**解决**:
```bash
# 发布静态 TF
ros2 run tf2_ros static_transform_publisher \
  --frame-id base_link \
  --child-frame-id laser_link
```

---

### 问题 C: Cartographer 报错 "No matching sensor data"

**原因**: 话题名称不匹配或数据类型错误

**解决**:
```bash
# 1. 检查话题名称
ros2 topic list | grep -E "scan|imu"

# 2. 检查数据类型
ros2 topic type /cx/laserscan
ros2 topic type /imu/data

# 3. 修改启动文件的 remappings
# 编辑：src/cartographer_config/launch/cartographer_2d_launch.py
```

---

### 问题 D: 有地图但很模糊或不完整

**原因**: Cartographer 参数配置不当

**解决**:
```lua
-- 修改 cartographer_2d.lua
TRAJECTORY_BUILDER_2D.min_range = 0.1      -- 最小距离
TRAJECTORY_BUILDER_2D.max_range = 50.0     -- 最大距离
TRAJECTORY_BUILDER_2D.use_imu_data = true  -- 使用 IMU
POSE_GRAPH.optimize_every_n_nodes = 30     -- 优化频率
```

---

## 📋 完整检查清单

启动前检查：
- [ ] 激光雷达驱动正常运行
- [ ] `/cx/points_raw` 话题有数据
- [ ] `/cx/laserscan` 话题有数据
- [ ] `/imu/data` 话题有数据
- [ ] TF 树完整 (map→odom→base_link→laser_link)
- [ ] Cartographer 节点启动
- [ ] occupancy_grid 节点启动
- [ ] RViz2 中添加 Map 显示

启动后检查：
- [ ] `/map` 话题有数据
- [ ] RViz2 中能看到地图
- [ ] Cartographer 日志无报错
- [ ] 轨迹正常构建

---

## 🎯 快速诊断脚本

创建诊断脚本 `diagnose_mapping.sh`:

```bash
#!/bin/bash

echo "=== ROS2 建图系统诊断 ==="
echo ""

echo "1. 检查关键话题:"
ros2 topic list | grep -E "points_raw|laserscan|imu"

echo ""
echo "2. 检查话题数据:"
echo "   /cx/points_raw:"
ros2 topic echo /cx/points_raw --once --timeout 1.0 > /dev/null && echo "   ✅ 有数据" || echo "   ❌ 无数据"

echo "   /cx/laserscan:"
ros2 topic echo /cx/laserscan --once --timeout 1.0 > /dev/null && echo "   ✅ 有数据" || echo "   ❌ 无数据"

echo "   /imu/data:"
ros2 topic echo /imu/data --once --timeout 1.0 > /dev/null && echo "   ✅ 有数据" || echo "   ❌ 无数据"

echo ""
echo "3. 检查 Cartographer 节点:"
ros2 node list | grep cartographer

echo ""
echo "4. 检查地图话题:"
ros2 topic echo /map --once --timeout 1.0 > /dev/null && echo "   ✅ 地图正常" || echo "   ❌ 无地图"

echo ""
echo "5. 检查 TF 树:"
ros2 run tf2_ros tf2_monitor 2>&1 | head -20
```

---

## 📞 调试支持

如果以上步骤都无法解决，请提供：

1. **话题列表**: `ros2 topic list`
2. **TF 树**: `ros2 run tf2_tools view_frames.py`
3. **Cartographer 日志**: 启动时的完整输出
4. **RViz2 截图**: 显示当前能看到的内容

---

*分析完成时间：2026-03-18 02:36 UTC*  
*分析者：绾绾*
