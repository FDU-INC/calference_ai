# 卫星通信干扰分析系统 - 微服务版

## 项目概述

本项目将原有的单体应用改造为微服务架构，提供卫星通信干扰分析功能。系统包含5个微服务和1个客户端程序，支持GSO和NGSO卫星系统的干扰分析，并集成了AI驱动的报告生成功能。

## 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   地面站服务     │    │    卫星服务      │    │    天线服务      │    │  干扰计算服务    │
│  Port: 5001     │    │  Port: 5002     │    │  Port: 5003     │    │  Port: 5004     │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │                       │
         └───────────────────────┼───────────────────────┼───────────────────────┘
                                 │                       │
                    ┌─────────────────┐    ┌─────────────────┐
                    │   主客户端程序   │    │   AI报告服务     │
                    │ main_client.py  │    │  Port: 5005     │
                    └─────────────────┘    └─────────────────┘
                                 │                       │
                    ┌─────────────────┐    ┌─────────────────┐
                    │   启动脚本      │    │   进程管理      │
                    │start_services.py│    │   统一控制      │
                    └─────────────────┘    └─────────────────┘
```

## 微服务说明

### 1. 地面站服务 (earth_station_service.py)

- **端口**: 5001
- **功能**: 地面站数据的增删改查
- **API接口**:
  - `GET /stations` - 获取所有地面站
  - `GET /stations/<id>` - 获取指定地面站
  - `POST /stations` - 创建地面站
  - `PUT /stations/<id>` - 更新地面站
  - `DELETE /stations/<id>` - 删除地面站
  - `GET /health` - 健康检查

### 2. 卫星服务 (satellites_service.py)

- **端口**: 5002
- **功能**: 卫星数据的增删改查
- **API接口**:
  - `GET /satellites` - 获取所有卫星
  - `GET /satellites/<id>` - 获取指定卫星
  - `POST /satellites` - 创建卫星
  - `PUT /satellites/<id>` - 更新卫星
  - `DELETE /satellites/<id>` - 删除卫星
  - `GET /health` - 健康检查

### 3. 天线服务 (antennas_service.py)

- **端口**: 5003
- **功能**: 天线数据的增删改查
- **API接口**:
  - `GET /antennas` - 获取所有天线
  - `GET /antennas/<id>` - 获取指定天线
  - `POST /antennas` - 创建天线
  - `PUT /antennas/<id>` - 更新天线
  - `DELETE /antennas/<id>` - 删除天线
  - `GET /health` - 健康检查

### 4. 干扰计算服务 (interference_service.py)

- **端口**: 5004
- **功能**: 核心干扰计算功能
- **API接口**:
  - `POST /compute_ci` - 计算载干比
  - `POST /check_itu_thresholds` - 检查ITU标准
  - `POST /update_ngso_interference` - NGSO干扰分析
  - `GET /health` - 健康检查
  - `GET /services/health` - 检查依赖服务状态

### 5. AI报告服务 (itu_report_generator/demo_ms.py)

- **端口**: 5005
- **功能**: AI驱动的干扰分析报告生成
- **API接口**:
  - `POST /analyze` - 生成AI分析报告
  - `GET /health` - 健康检查
- **特性**:
  - 多智能体系统
  - 支持图像分析
  - 生成Markdown和Word文档

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动所有微服务

```bash
# 使用启动脚本（推荐）
python start_services.py
```

启动脚本功能：

- 自动启动所有5个微服务
- 进程管理和监控
- 统一停止所有服务（Ctrl+C）

### 3. 运行主客户端程序

```bash
python main_client.py
```

客户端功能：

- 服务健康检查
- 数据加载（可选）
- 干扰分析（可选）
- AI报告生成

## 使用示例

### 1. 创建地面站

```bash
curl -X POST http://localhost:5001/stations \
  -H "Content-Type: application/json" \
  -d '{
    "station_id": "BEIJING_GS",
    "name": "北京地面站",
    "lat_deg": 39.9042,
    "lon_deg": 116.4074,
    "alt_m": 50,
    "rx_system": {
      "T_sys_K": 500,
      "bandwidth_Hz": 36000000,
      "rx_losses_dB": 1.5
    },
    "rx_antenna_id": "ANT_RX_1"
  }'
```

### 2. 创建卫星

```bash
curl -X POST http://localhost:5002/satellites \
  -H "Content-Type: application/json" \
  -d '{
    "satellite_id": "GSO_A",
    "name": "GSO_A",
    "lon_deg": 123.0,
    "tx_eirp_dBW": 45.0,
    "tx_losses_dB": 1.0,
    "frequency_Hz": 12000000000
  }'
```

### 3. 计算载干比

```bash
curl -X POST http://localhost:5004/compute_ci \
  -H "Content-Type: application/json" \
  -d '{
    "station_id": "BEIJING_GS",
    "main_satellite_id": "GSO_A",
    "interf_satellite_id": "GSO_B",
    "verbose": true
  }'
```

### 4. 生成AI报告

```bash
curl -X POST http://localhost:5005/analyze \
  -F "image_name=oneweb_total_earth_cinr.png" \
  -F "download=false"
```

## 文件结构

```
项目根目录/
├── earth_station_service.py      # 地面站微服务
├── satellites_service.py         # 卫星微服务
├── antennas_service.py           # 天线微服务
├── interference_service.py       # 干扰计算微服务
├── main_client.py               # 主客户端程序
├── start_services.py            # 服务启动脚本
├── requirements.txt             # 依赖文件
├── README_微服务版.md           # 说明文档
├── itu_report_generator/        # AI报告生成器
│   ├── demo_ms.py              # AI报告微服务
│   ├── demo.py                 # 核心AI逻辑
│   └── data/                   # 报告数据目录
├── earth_station.py             # 原有地面站模块
├── satellites.py                # 原有卫星模块
├── antennas.py                  # 原有天线模块
├── interference.py              # 原有干扰计算模块
├── main.py                      # 原有主程序
└── *.json                       # 数据文件
```

## 微服务优势

1. **模块化**: 每个服务职责单一，便于维护
2. **可扩展**: 可以独立扩展某个服务
3. **容错性**: 单个服务故障不影响其他服务
4. **技术栈灵活**: 每个服务可以使用不同的技术栈
5. **部署独立**: 可以独立部署和更新
6. **AI集成**: 支持智能报告生成

## 注意事项

1. **端口冲突**: 确保5001-5005端口未被占用
2. **依赖顺序**: 干扰计算服务依赖其他三个服务
3. **数据一致性**: 微服务间通过API调用，需要处理数据一致性问题
4. **错误处理**: 客户端需要处理服务不可用的情况
5. **性能**: 微服务间通信会有一定的性能开销
6. **AI服务**: AI报告服务需要较长的初始化时间

## 故障排除

### 1. 服务启动失败

- 检查端口是否被占用
- 检查依赖是否正确安装
- 查看错误日志

### 2. 服务间通信失败

- 检查服务是否正常运行
- 检查网络连接
- 使用健康检查接口

### 3. 数据加载失败

- 检查JSON文件是否存在
- 检查文件格式是否正确
- 检查服务依赖关系

### 4. AI报告生成失败

- 检查AI服务是否完全启动
- 检查图像文件是否存在
- 检查网络连接和超时设置

## 扩展功能

1. **服务发现**: 可以集成Consul或Eureka
2. **负载均衡**: 可以添加Nginx或HAProxy
3. **监控**: 可以集成Prometheus和Grafana
4. **日志**: 可以集成ELK栈
5. **容器化**: 可以使用Docker和Kubernetes
6. **AI增强**: 可以集成更多AI模型和功能

## 快速命令

```bash
# 启动所有服务
python start_services.py

# 运行分析
python main_client.py

# 停止所有服务
Ctrl+C (在启动脚本终端中)

# 强制停止所有Python进程
taskkill /F /IM python.exe
```
