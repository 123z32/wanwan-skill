# 🔍 Cartographer 建图失败深度排查报告

**分析时间**: 2026-03-18 02:50 UTC  
**问题**: 只有激光点图，没有地图生成  
**TF 状态**: ✅ 已确认正常

---

## 🚨 新发现的 5 个潜在问题

### 问题 1: Cartographer 话题 remapping 错误 ⚠️⚠️⚠️

**启动文件配置**:
```python
remappings=[
    ('scan', '/cx/laserscan'),    # 重映射 scan → /cx/laserscan
    ('imu', '/imu/data')          # 重映射 imu → /imu/data
]
```

**问题分析**:
- Cartographer 期望的话题名是 `scan` 和 `imu`
- 重映射后实际订阅 `/cx/laserscan` 和 `/imu/data`
- **但是**: 需要确认这些话题**真的有数据且类型正确**

**检查命令**:
```bash
# 1. 检查话题是否存在
ros2 topic list | grep -E "scan|imu"

# 2. 检查话题类型
ros2 topic type /cx/laserscan
# 应该输出：sensor_msgs/msg/LaserScan

ros2 topic type /imu/data
# 应该输出：sensor_msgs/msg/Imu

# 3. 检查话题数据
ros2 topic echo /cx/laserscan --once --timeout 2.0
ros2 topic echo /imu/data --once --timeout 2.0

# 4. 检查话题频率
ros2 topic hz /cx/laserscan
ros2 topic hz /imu/data
```

**期望输出**:
- `/cx/laserscan`: 10Hz LaserScan
- `/imu/data`: 50-100Hz Imu

---

### 问题 2: Cartographer 节点日志报错 ⚠️⚠️⚠️

**可能的错误信息**:

**错误 A**: "No matching sensor data received"
**原因**: 话题名称不匹配或数据类型错误
**解决**: 
```bash
# 检查 Cartographer 实际订阅的话题
ros2 node info /cartographer_node
```

**错误 B**: "Frame id map not found in lookup transform"
**原因**: TF 树不完整
**解决**: 已确认 TF 正常，跳过

**错误 C**: "Trajectory building failed"
**原因**: 激光数据质量差或参数配置不当
**解决**: 调整 Lua 配置参数

---

### 问题 3: occupancy_grid 节点未启动 ⚠️⚠️

**关键发现**: 启动文件中有 `occupancy_grid_node`，但实际可能没运行！

**检查方法**:
```bash
# 检查节点列表
ros2 node list | grep occupancy

# 检查/map 话题
ros2 topic list | grep map

# 如果没有/map 话题，说明 occupancy_grid 节点没运行
```

**occupancy_grid 节点的作用**:
- 订阅 Cartographer 的内部地图数据
- 发布标准的 `/map` 话题 (OccupancyGrid)
- **没有它，Cartographer 不会发布/map 话题！**

**手动启动**:
```bash
ros2 run cartographer_ros cartographer_occupancy_grid_node \
  --ros-args -p resolution:=0.05
```

---

### 问题 4: Lua 配置参数过于严格 ⚠️

**当前配置**:
```lua
TRAJECTORY_BUILDER_2D.min_range = 0.1      -- 最小 0.1 米
TRAJECTORY_BUILDER_2D.max_range = 50.0     -- 最大 50 米
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 5.0  -- 缺失数据处理
POSE_GRAPH.optimize_every_n_nodes = 30     -- 每 30 个节点优化一次
```

**潜在问题**:
- `missing_data_ray_length = 5.0` 可能导致建图失败
- `optimize_every_n_nodes = 30` 可能太大，导致建图延迟

**建议修改**:
```lua
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 1.0  -- 减小缺失数据处理
POSE_GRAPH.optimize_every_n_nodes = 10     -- 更频繁的优化
```

---

### 问题 5: 激光雷达数据质量问题 ⚠️

**需要检查**:
1. 激光雷达是否真的在发布数据？
2. 数据格式是否正确？
3. 数据范围是否合理？

**检查命令**:
```bash
# 查看激光雷达数据详情
ros2 topic echo /cx/laserscan --once

# 重点检查:
# - ranges 数组是否有有效数据
# - ranges 中的值是否在合理范围 (0.1-50.0 米)
# - 是否有大量 inf 或 nan 值
```

**期望输出示例**:
```yaml
header:
  stamp: {sec: 123, nanosec: 456}
  frame_id: laser_link
angle_min: -3.14
angle_max: 3.14
angle_increment: 0.017
ranges: [1.5, 2.3, 1.8, ..., 2.1]  # ← 应该有有效数据
```

**常见问题**:
- `ranges` 全是 `inf` → 激光雷达没检测到障碍物
- `ranges` 全是 `0.0` → 数据异常
- `ranges` 长度不对 → 角度配置错误

---

## 🔧 完整排查流程

### 步骤 1: 检查所有节点是否运行

```bash
# 列出所有节点
ros2 node list

# 应该看到:
# - /cartographer_node
# - /occupancy_grid_node
# - /lslidar_driver_node (或类似)
# - /single_lidar_dispose
```

**如果缺少 occupancy_grid_node**:
```bash
# 手动启动
ros2 run cartographer_ros cartographer_occupancy_grid_node \
  --ros-args -p resolution:=0.05
```

---

### 步骤 2: 检查 Cartographer 订阅的话题

```bash
# 查看 Cartographer 节点信息
ros2 node info /cartographer_node

# 输出示例:
# /cartographer_node
#   Subscribers:
#     /scan: sensor_msgs/msg/LaserScan    ← 检查这个话题
#     /imu: sensor_msgs/msg/Imu           ← 检查这个话题
```

**如果话题不匹配**:
```bash
# 修改启动文件的 remappings
# 编辑：src/cartographer_config/launch/cartographer_2d_launch.py
```

---

### 步骤 3: 检查 Cartographer 日志

```bash
# 启动 Cartographer 并查看详细日志
ros2 launch cartographer_config cartographer_2d_launch.py 2>&1 | tee /tmp/cartographer.log

# 搜索错误信息
grep -i "error\|warning\|failed" /tmp/cartographer.log
```

**常见错误及解决**:

**错误**: "No valid transforms"
**解决**: 检查 TF 树

**错误**: "Dropped message"
**解决**: 检查话题频率和数据量

**错误**: "Trajectory 0 finished"
**解决**: 建图完成，需要保存地图

---

### 步骤 4: 手动触发建图测试

```bash
# 1. 启动所有节点后，等待 30 秒

# 2. 检查 Cartographer 状态
ros2 service list | grep cartographer

# 3. 查询轨迹状态
ros2 service call /trajectory_query \
  cartographer_ros_msgs/srv/TrajectoryQuery \
  "{trajectory_id: 0}"

# 4. 如果有数据返回，说明建图正常
```

---

### 步骤 5: 检查 RViz2 显示

```bash
# 启动 RViz2
ros2 run rviz2 rviz2
```

**添加显示项**:
1. **LaserScan** - Topic: `/cx/laserscan`
   - ✅ 应该看到激光扫描线
   
2. **Map** - Topic: `/map`
   - ❌ 如果没有显示，说明 occupancy_grid 节点没运行
   
3. **TF** - 显示坐标变换
   - ✅ 应该看到完整的 TF 树

---

## 🎯 快速诊断脚本

创建 `diagnose_cartographer.sh`:

```bash
#!/bin/bash

echo "=== Cartographer 建图诊断 ==="
echo ""

echo "1. 检查节点:"
ros2 node list | grep -E "cartographer|occupancy"

echo ""
echo "2. 检查话题:"
ros2 topic list | grep -E "scan|map|imu"

echo ""
echo "3. 检查激光数据:"
if ros2 topic echo /cx/laserscan --once --timeout 1.0 > /dev/null 2>&1; then
    echo "   ✅ /cx/laserscan 有数据"
    # 检查 ranges 数组
    ranges=$(ros2 topic echo /cx/laserscan --once 2>&1 | grep -A 5 "ranges:")
    if echo "$ranges" | grep -q "inf"; then
        echo "   ⚠️ 警告：ranges 包含 inf 值"
    else
        echo "   ✅ ranges 数据正常"
    fi
else
    echo "   ❌ /cx/laserscan 无数据"
fi

echo ""
echo "4. 检查 IMU 数据:"
if ros2 topic echo /imu/data --once --timeout 1.0 > /dev/null 2>&1; then
    echo "   ✅ /imu/data 有数据"
else
    echo "   ❌ /imu/data 无数据"
fi

echo ""
echo "5. 检查地图话题:"
if ros2 topic echo /map --once --timeout 1.0 > /dev/null 2>&1; then
    echo "   ✅ /map 有数据 (建图正常)"
else
    echo "   ❌ /map 无数据 (建图失败)"
    echo "   可能原因：occupancy_grid 节点未运行"
fi

echo ""
echo "6. 检查 Cartographer 日志:"
ros2 launch cartographer_config cartographer_2d_launch.py 2>&1 | \
  grep -i "error\|warning" | head -10
```

---

## 📋 最可能的 3 个原因

根据经验，建图失败最常见的原因：

### 1. occupancy_grid 节点未运行 (80% 可能性)

**症状**: 
- Cartographer 节点正常运行
- 激光数据显示正常
- 但没有 `/map` 话题

**解决**:
```bash
ros2 run cartographer_ros cartographer_occupancy_grid_node &
```

---

### 2. 话题 remapping 不匹配 (15% 可能性)

**症状**:
- Cartographer 报错 "No matching sensor data"
- 话题存在但 Cartographer 收不到

**解决**:
```bash
# 检查 Cartographer 实际订阅的话题
ros2 node info /cartographer_node

# 修改启动文件的 remappings
# 确保话题名称完全匹配
```

---

### 3. 激光数据质量差 (5% 可能性)

**症状**:
- `ranges` 数组全是 `inf` 或 `0.0`
- 激光雷达没检测到障碍物

**解决**:
```bash
# 检查激光雷达硬件
# 检查前方是否有障碍物
# 调整 min_range 和 max_range 参数
```

---

## 📞 请提供以下信息

如果以上排查都无法解决，请提供：

1. **节点列表**:
   ```bash
   ros2 node list
   ```

2. **话题列表**:
   ```bash
   ros2 topic list
   ```

3. **Cartographer 日志** (前 50 行):
   ```bash
   ros2 launch cartographer_config cartographer_2d_launch.py 2>&1 | head -50
   ```

4. **激光数据样例**:
   ```bash
   ros2 topic echo /cx/laserscan --once
   ```

5. **RViz2 截图**: 显示当前能看到的内容

---

*分析完成时间：2026-03-18 02:50 UTC*  
*分析者：绾绾*
