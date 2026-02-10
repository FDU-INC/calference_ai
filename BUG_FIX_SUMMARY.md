# Bug 修复总结

## 问题描述
运行仿真时出现错误：
```
❌ 错误: API Error 500: {"detail":"unsupported operand type(s) for -: 'datetime.time' and 'datetime.time'"}
```

## 根本原因
在 `Calself/earth_station.py` 的 `update_earth_stations()` 函数中，参数名为 `time`，这覆盖了 Python 的 `time` 模块。

当代码执行到 `time.time()` 时，实际上是在调用参数对象的 `time()` 方法（因为参数是 `datetime` 对象），而不是 `time` 模块的 `time()` 函数。这导致：
- `time.time()` 返回 `datetime.time` 对象而不是浮点数
- 在计算执行时间时进行减法操作：`end_time_function - start_time_function`
- 两个 `datetime.time` 对象无法进行减法操作，导致错误

## 修复方案
将参数名从 `time` 改为 `sim_time`，避免与 `time` 模块名冲突。

### 修改的文件
- `Calself/earth_station.py`

### 修改的函数
- `update_earth_stations(earth_stations, sim_time, earth_stations_index)`

### 具体改动
```python
# 修改前
def update_earth_stations(earth_stations, time, earth_stations_index):
    start_time_function = time.time()  # ❌ 调用参数的 time() 方法
    ...
    end_time_function = time.time()
    execution_time = end_time_function - start_time_function  # ❌ datetime.time - datetime.time

# 修改后
def update_earth_stations(earth_stations, sim_time, earth_stations_index):
    import time as time_module
    start_time_function = time_module.time()  # ✅ 调用 time 模块的 time() 函数
    ...
    end_time_function = time_module.time()
    execution_time = end_time_function - start_time_function  # ✅ float - float
```

## 验证
- ✅ Python 语法检查通过
- ✅ 函数签名正确
- ✅ 参数类型匹配

## 相关最佳实践
1. **避免使用内置模块名作为参数名**
   - ❌ `def func(time, os, sys):`
   - ✅ `def func(sim_time, output_dir, system_config):`

2. **使用明确的参数名**
   - ❌ `time` (模糊，可能是时间戳、时间对象或时间模块)
   - ✅ `sim_time` (清晰表示这是仿真时间)

3. **导入模块时使用别名避免冲突**
   ```python
   import time as time_module
   ```

## 测试建议
运行以下命令测试修复：
```bash
# 启动 Calself 微服务
python run.py calself-service --port 8001

# 在另一个终端运行仿真
python run.py calself-sim --duration 0.1 --step 2
```

## 相关文件
- `Calself/earth_station.py:777` - update_earth_stations 函数
- `Calself/main_ms.py:186` - 调用 update_earth_stations 的位置
