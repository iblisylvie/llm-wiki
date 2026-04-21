# 智算中心后端API参考文档

## 概述

本文档描述智算中心后端所有可用的API接口。

**基础URL**: `http://localhost:8002`
**线上URL**: `https://gaidc.seraphimpower.com.cn`

## 认证

除了登录接口外，所有API都需要Bearer Token认证：

```bash
# 1. 登录获取token
curl -s -X POST 'http://localhost:8002/api/v1/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{"username": "admin", "password": "admin123"}'

# 2. 使用token
curl -s 'http://localhost:8002/api/v1/xxx' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

**用户角色**:
| 角色 | 用户名/密码 | 权限范围 |
|------|------------|---------|
| 系统管理员 | admin/admin123 | 全部功能 |
| 运维工程师 | operator/operator123 | 能源/算力监控、告警 |
| 管理层 | manager/manager123 | 仪表板、ESG、账单 |
| 客户 | customer/customer123 | 个人使用、账单 |

---

### 登录
```
POST /api/v1/auth/login
Content-Type: application/json

请求体:
{
  "username": "admin",
  "password": "admin123"
}

返回:
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user_info": {
    "username": "admin",
    "role": "系统管理员",
    "permissions": ["all"]
  }
}
```

### 获取当前用户档案
```
GET /api/v1/auth/profile
Authorization: Bearer TOKEN

返回:
{
  "username": "admin",
  "role": "系统管理员",
  "full_name": null,
  "email": null,
  "avatar": null,
  "last_login": null,
  "permissions": ["all"]
}
```

### 用户登出
```
POST /api/v1/auth/logout
Authorization: Bearer TOKEN

返回:
{
  "message": "登出成功",
  "username": "admin",
  "timestamp": "2026-03-20T15:30:00"
}
```

### 获取用户权限
```
GET /api/v1/auth/permissions
Authorization: Bearer TOKEN

返回:
{
  "username": "admin",
  "role": "系统管理员",
  "permissions": ["dashboard", "energy", "compute", "es_green", "cluster", "billing", "alerts", "strategies"]
}
```

### 修改密码（管理员）
```
POST /api/v1/auth/change-password?current_password=xxx&new_password=xxx
Authorization: Bearer TOKEN

查询参数:
- current_password: 当前密码 (必填)
- new_password: 新密码 (必填)

返回:
{
  "message": "密码修改成功",
  "username": "admin",
  "timestamp": "2026-03-20T15:30:00"
}
```

### 获取用户列表(管理员)
```
GET /api/v1/auth/users
Authorization: Bearer TOKEN
需要管理员权限

返回:
{
  "users": [
    {
      "username": "admin",
      "role": "系统管理员",
      "email": null,
      "is_active": true
    }
  ],
  "total": 4,
  "timestamp": "2026-03-20T15:30:00"
}
```

---

## 2. 账单模块 `/api/v1/billing`

### 2.1 日账单子模块 `/api/v1/billing/daily`

#### 当日实时账单
```
GET /api/v1/billing/daily/current
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "data": {
    "date": "2026-03-20",
    "current_kwh": 8500.5,        // 今日累计用电量 (kWh)
    "current_cost": 3825.25,      // 今日累计电费 (元)
    "last_update": "2026-03-20T15:30:00",
    "is_simulated": false
  }
}
```

#### 历史账单列表
```
GET /api/v1/billing/daily/history/list
Authorization: Bearer TOKEN

参数:
- start_date: 开始日期 (YYYY-MM-DD, 可选)
- end_date: 结束日期 (YYYY-MM-DD, 可选)
- page: 页码 (默认1)
- page_size: 每页数量 (默认30, 最大100)

返回:
{
  "success": true,
  "data": {
    "bills": [
      {
        "date": "2026-03-14",
        "total_kwh": 12500.5,
        "total_cost": 5623.45,
        "is_valid": true,
        "cost_difference_rate": 0.02
      }
    ],
    "pagination": { "page": 1, "page_size": 30, "total": 7 },
    "statistics": { "total_kwh": 87500, "total_cost": 39000 }
  }
}
```

#### 指定日期账单
```
GET /api/v1/billing/daily/{date}
Authorization: Bearer TOKEN
路径参数: date (YYYY-MM-DD)

返回:
{
  "success": true,
  "data": {
    "date": "2026-03-19",
    "total_kwh": 12500.5,
    "total_cost": 5623.45,
    "cost_method_a": 5623.45,
    "cost_method_b": 5500.00,
    "is_simulated": false
  }
}
```

#### 账单统计
```
GET /api/v1/billing/daily/stats
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "data": {
    "total_bills": 30,
    "total_kwh": 375000,
    "total_cost": 168750,
    "avg_daily_kwh": 12500,
    "avg_daily_cost": 5625
  }
}
```

#### 重新计算账单（管理员）
```
POST /api/v1/billing/daily/recalculate?date=YYYY-MM-DD
Authorization: Bearer TOKEN
需要管理员权限

返回:
{
  "success": true,
  "message": "重新计算完成",
  "data": {
    "results": [{"date": "2026-03-19", "status": "success", "kwh": 12500, "cost": 5623}]
  }
}
```

### 2.2 账单总览与明细

#### 当前账单总览
```
GET /api/v1/billing/current/overview
Authorization: Bearer TOKEN

返回:
{
  "current_month": "2024-11",
  "total_amount": 12500.50,
  "gpu_costs": 8000.00,
  "energy_costs": 3000.00,
  "storage_costs": 1000.00,
  "other_costs": 500.50,
  "savings": 1500.00,
  "usage_increase": 10.5,
  "next_month_estimate": 13500.00
}
```

#### 费用构成
```
GET /api/v1/billing/current/breakdown
Authorization: Bearer TOKEN

返回:
{
  "total": 12500.50,
  "categories": [
    {"name": "GPU计算", "value": 8000.00, "color": "#3B82F6"},
    {"name": "能源消耗", "value": 3000.00, "color": "#10B981"},
    {"name": "存储服务", "value": 1000.00, "color": "#F59E0B"},
    {"name": "网络带宽", "value": 500.50, "color": "#8B5CF6"}
  ]
}
```

#### 账单明细
```
GET /api/v1/billing/current/details
Authorization: Bearer TOKEN

参数:
- category: 分类 (可选)
- page: 页码 (默认1)
- page_size: 每页数量 (默认20)
- date_from: 开始日期 (可选)
- date_to: 结束日期 (可选)

返回:
{
  "details": [
    {
      "id": "billing-0001",
      "date": "2024-11-15T10:30:00",
      "category": "GPU计算",
      "subcategory": "A100 GPU",
      "description": "资源使用费用 - 项目1",
      "amount": 500.00,
      "usage_hours": 24,
      "unit_price": 3.50,
      "status": "已计费"
    }
  ],
  "pagination": {"page": 1, "page_size": 20, "total": 100, "total_pages": 5}
}
```

#### 账单明细（高级查询）
```
GET /api/v1/billing/details
Authorization: Bearer TOKEN

参数:
- category: 分类 (可选)
- subcategory: 子分类 (可选)
- date_from: 开始日期 (可选)
- date_to: 结束日期 (可选)
- task_id: 任务ID (可选)
- user_id: 用户ID (可选)
- department: 部门 (可选)
- page: 页码 (默认1)
- page_size: 每页数量 (默认20)

返回: 与/billing/current/details格式类似的账单明细列表
```

#### 账单历史
```
GET /api/v1/billing/history
Authorization: Bearer TOKEN

参数:
- page: 页码 (默认1)
- page_size: 每页数量 (默认10)
- year: 年份 (可选)
- status: 状态 (可选)

返回:
{
  "history": [
    {
      "id": "bill-0001",
      "month": "2024-10",
      "total_amount": 12000.00,
      "status": "已支付",
      "payment_date": "2024-11-15T00:00:00",
      "usage_summary": {"gpu_hours": 500, "energy_kwh": 3000, "storage_gb": 200}
    }
  ],
  "pagination": {"page": 1, "page_size": 10, "total": 12, "total_pages": 2}
}
```

#### 成本趋势
```
GET /api/v1/billing/trends
Authorization: Bearer TOKEN

参数:
- period: 时间范围 (默认12months)
- category: 分类 (可选)

返回:
{
  "trends": [
    {
      "month": "2024-11",
      "total_cost": 12500.00,
      "gpu_cost": 8000.00,
      "energy_cost": 3000.00,
      "storage_cost": 1000.00,
      "other_cost": 500.00
    }
  ]
}
```

#### 费用预测
```
GET /api/v1/billing/current/forecast
Authorization: Bearer TOKEN

参数:
- confidence_level: 置信水平 (默认0.8)

返回:
{
  "predictedAmount": 13500.00,
  "confidenceInterval": 80,
  "contributingFactors": [
    {"name": "GPU使用量增加", "impact": 5.2}
  ],
  "optimizationPotential": 1080.00
}
```

#### 成本分析
```
GET /api/v1/billing/analysis/{period}
Authorization: Bearer TOKEN

返回:
{
  "breakdown": {"total": 12500.50, "categories": [...]},
  "recommendations": [
    {"title": "优化GPU调度策略", "priority": "high", "potentialSavings": 1500.00}
  ],
  "budget": {"annual": 150000, "used": 12500, "remaining": 137500, "usagePercentage": 8.3},
  "efficiency": {"costEfficiencyScore": 85.5, "gpuUtilization": 78.2, "greenEnergyRatio": 45.3}
}
```

#### 成本预警
```
GET /api/v1/billing/alerts
Authorization: Bearer TOKEN

返回:
{
  "alerts": [
    {
      "id": "alert-1",
      "type": "budget",
      "severity": "high",
      "title": "预算预警",
      "message": "本月支出已超过预算80%",
      "currentValue": 10000,
      "threshold": 8000,
      "triggeredAt": "2024-11-15T10:00:00",
      "resolved": false
    }
  ]
}
```

#### 实时费用
```
GET /api/v1/billing/realtime
Authorization: Bearer TOKEN

返回:
{
  "gpu_a100_rate": 3.85,
  "green_energy_rate": 0.68,
  "hot_storage_rate": 0.95,
  "active_gpus": 16,
  "power_usage": 250,
  "storage_usage": 1.5,
  "daily_forecast": 3800
}
```

#### 账单统计
```
GET /api/v1/billing/statistics
Authorization: Bearer TOKEN

参数:
- period: 时间范围 (current_month/last_month 等, 默认current_month)
- group_by: 分组方式 (category/user 等, 默认category)

返回:
{
  "daily_total": 5623.45,
  "daily_count": 45
}
```

---

## 3. 能源模块 `/api/v1/energy`

### 实时能源数据
```
GET /api/v1/energy/realtime
Authorization: Bearer TOKEN

返回:
{
  "timestamp": "2026-03-20T15:30:00",
  "solar_power": 75.2,      // 光伏出力 (kW)
  "wind_power": 45.8,       // 风电出力 (kW)
  "grid_power": 120.5,      // 电网功率 (kW)
  "storage_soc": 65.3,      // 储能SOC (%)
  "total_load": 241.5,      // 总负载 (kW)
  "price": 0.85,            // 当前电价 (元/kWh)
  "contract_power": 200.0   // 合同容量 (kW)
}
```

### 能源历史数据
```
GET /api/v1/energy/history?hours=24
Authorization: Bearer TOKEN

返回:
[
  {
    "timestamp": "2026-03-20T14:00:00",
    "solar_power": 75.2,
    "wind_power": 45.8,
    "grid_power": 120.5,
    "storage_soc": 65.3,
    "total_load": 241.5,
    "price": 0.85
  }
]
```

### 储能收益（实时）
```
GET /api/v1/energy/storage-revenue/realtime
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "data": {
    "daily_revenue": 7371.56,        // 今日收益 (元)
    "monthly_revenue": 221146.71,    // 本月累计 (元)
    "discharge_kwh": 12785.97,       // 放电电量 (kWh)
    "avg_savings_per_kwh": 0.58,     // 平均每度电节省 (元)
    "discharge_count": 9894          // 放电次数
  }
}
```

### 削峰填谷指标
```
GET /api/v1/energy/peak-shaving/daily-metrics?date=YYYY-MM-DD
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "data": {
    "peak_shaving_power_kw": 1500,
    "peak_shaving_energy_kwh": 2500,
    "valley_filling_power_kw": 1200,
    "valley_filling_energy_kwh": 2000,
    "peak_period_discharge_kwh": 2500,
    "valley_period_charge_kwh": 2000
  }
}
```

### 噶能系统信息
```
GET /api/v1/energy/storage
Authorization: Bearer TOKEN

返回:
{
  "current_soc": 65.5,           // 当前SOC (%)
  "capacity": 1000.0,            // 总容量 (kWh)
  "current_charge": 655.0,      // 当前电量 (kWh)
  "charging_rate": 50.0,    // 充放电功率 (kW)
  "efficiency": 0.9,            // 效率
  "cycle_count": 350,        // 循环次数
  "health_status": "良好",   // 健康状态
  "last_maintenance": "2024-10-15T10:00:00Z"
}
```

### 实时负载与预测
```
GET /api/v1/energy/load-forecast/realtime?date=YYYY-MM-DD
Authorization: Bearer TOKEN

参数:
- date: 日期 (YYYY-MM-DD, 可选)

返回:
{
  "success": true,
  "data": {
    "realtime_load_kw": 350.5,
    "predicted_load_kw": 345.0,
    "timestamp": "2026-03-20T15:30:00"
  }
}
```

### 负载预测概要
```
GET /api/v1/energy/load-forecast/summary?date=YYYY-MM-DD
Authorization: Bearer TOKEN

路径参数: date (YYYY-MM-DD, 必填)

返回:
{
  "success": true,
  "data": {
    "date": "2026-03-20",
    "total_points": 96,
    "avg_predicted_load_kw": 320.5,
    "peak_load_kw": 450.0,
    "min_load_kw": 180.0
  }
}
```

### 负载预测数据
```
GET /api/v1/energy/load-forecast/data?hours=24
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "data": {
    "forecast_data": [
      {
        "timestamp": "2026-03-20T15:00:00",
        "predicted_load_kw": 150.5,
        "actual_load_value": 148.2
      }
    ],
    "total_points": 96,
    "hours": 24
  }
}
```

### 历史负载数据
```
GET /api/v1/energy/load-forecast/history?hours=24&granularity_minutes=10
Authorization: Bearer TOKEN

参数:
- hours: 时间范围 (1-168, 默认24)
- granularity_minutes: 粒度 (1-60, 默认10)

返回:
{
  "success": true,
  "data": {
    "history_data": [
      {"timestamp": "2026-03-20T15:00:00", "power_kw": 350.5}
    ],
    "total_points": 144,
    "hours": 24,
  }
}
```

### 测试负载预测连接
```
GET /api/v1/energy/load-forecast/test
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "data": {
    "external_service_connected": true,
    "cache_info": {"size": 10, "ttl": 60},
    "test_timestamp": "2026-03-20T15:30:00"
  }
}
```

### 指定日期储能收益
```
GET /api/v1/energy/storage-revenue/daily?date=YYYY-MM-DD
Authorization: Bearer TOKEN

参数:
- date: 日期 (YYYY-MM-DD, 可选，默认今天)
- site_id: 站点ID (可选)

返回:
{
  "success": true,
  "data": {
    "date": "2026-03-20",
    "daily_revenue": 7371.56,
    "monthly_revenue": 221146.71,
    "discharge_kwh": 12785.97,
    "avg_savings_per_kwh": 0.58
  }
}
```

### 能源预测

#### 超短期预测（4小时，15分钟步进）
```
GET /api/v1/energy/forecast/ultra?hours=4&site_id=xxx
Authorization: Bearer TOKEN

返回:
{
  "timestamp": "2026-03-20T15:30:00Z",
  "data_source": "real_external",
  "forecast": [...]
}
```

#### 短期预测（48小时，15分钟步进）
```
GET /api/v1/energy/forecast/short?hours=48
Authorization: Bearer TOKEN

返回: 同上格式
```

#### 中期预测（7天，1小时步进）
```
GET /api/v1/energy/forecast/mid?days=7
Authorization: Bearer TOKEN

返回: 同上格式
```

#### 长期预测（30天，1天步进）
```
GET /api/v1/energy/forecast/long?days=30
Authorization: Bearer TOKEN

返回: 同上格式
```

#### 预测概要
```
GET /api/v1/energy/forecast/summary?site_id=shanghai_jiading
Authorization: Bearer TOKEN

返回:
{
  "timestamp": "2026-03-20T15:30:00Z",
  "data_source": "real_external",
  "summary": {...}
}
```

---

## 4. 扩展能源模块 `/api/v1/energy-extended`

### 储能系统状态
```
GET /api/v1/energy-extended/storage-status
Authorization: Bearer TOKEN

返回:
{
  "soc": 65.3,
  "charge_power": 0.0,
  "discharge_power": 50.0,
  "battery_health": 95.0,
  "temperature": 25.0,
  "capacity": 20000.0,
  "available_capacity": 13060.0,
  "strategy": {
    "charge_threshold": 0.1,
    "discharge_threshold": 0.9,
    "efficiency": 0.9
  }
}
```

### 当前电价
```
GET /api/v1/energy-extended/electricity-price/current
Authorization: Bearer TOKEN

返回:
{
  "timestamp": "2026-03-20T15:30:00",
  "price_type": "peak",
  "current_price": 0.85,
  "tou_price": 0.82,
  "spot_price": 0.80,
  "contract_price": 0.45
}
```

### 电价预测
```
GET /api/v1/energy-extended/electricity-price/forecast?hours=24
Authorization: Bearer TOKEN

返回:
[
  {
    "timestamp": "2026-03-20T16:00:00",
    "price_type": "normal",
    "tou_price": 0.65,
    "current_price": 0.65
  }
]
```

### 电价与负载叠加
```
GET /api/v1/energy-extended/price-load-overlay?hours=24
Authorization: Bearer TOKEN

返回:
{
  "data": [
    {
      "timestamp": "2026-03-20T00:00:00",
      "tou_price": 0.42,
      "load": 35.8,
      "scheduling_events": []
    }
  ],
  "summary": {
    "average_price": 0.51,
    "max_load": 150.5
  }
}
```

### 功率曲线历史
```
GET /api/v1/energy-extended/power-curve/history?hours=24&granularity_minutes=60
Authorization: Bearer TOKEN

返回:
[
  {
    "timestamp": "2026-03-20T14:00:00",
    "solar_power": 75.2,
    "wind_power": 0.0,
    "grid_power": 120.5,
    "storage_charge_power": 0.0,
    "storage_discharge_power": 50.0,
    "total_load": 241.5,
    "price": 0.65,
    "electricity_price_type": "tou",
    "renewable_soc_ratio": 0.65
  }
]
```

### 系统健康状态
```
GET /api/v1/energy-extended/system-health
Authorization: Bearer TOKEN

返回:
{
  "overall_status": "normal",
  "overall_score": 92.5,
  "components": [...],
  "alerts": [...]
}
```

### 实时能源数据
```
GET /api/v1/energy-extended/realtime
Authorization: Bearer TOKEN

返回: 实时能源综合数据
```

### 能源历史数据
```
GET /api/v1/energy-extended/history?hours=24&city=shanghai
Authorization: Bearer TOKEN

参数:
- hours: 时间范围 (默认24)
- city: 城市 (可选)

返回: 历史能源数据列表
```

### 电价时段计划
```
GET /api/v1/energy-extended/electricity-price/schedule?date=YYYY-MM-DD&interval_minutes=60
Authorization: Bearer TOKEN

参数:
- date: 日期 (可选)
- interval_minutes: 间隔分钟 (默认60)

返回: 电价时段计划
```

### 负载预测
```
GET /api/v1/energy-extended/load-forecast?hours=24
Authorization: Bearer TOKEN

参数:
- hours: 预测时长 (默认24)

返回: 负载预测数据
```

### 能源构成
```
GET /api/v1/energy-extended/energy-composition?hours=24
Authorization: Bearer TOKEN

参数:
- hours: 时间范围 (默认24)

返回: 各能源类型占比数据
```

### 关键指标
```
GET /api/v1/energy-extended/key-metrics
Authorization: Bearer TOKEN

返回: 能源系统关键指标汇总
```

### 调度建议
```
GET /api/v1/energy-extended/scheduling-recommendations
Authorization: Bearer TOKEN

返回: 智能调度建议
```

### ESG指标
```
GET /api/v1/energy-extended/esg-metrics
Authorization: Bearer TOKEN

返回: ESG相关指标数据
```

### 系统告警
```
GET /api/v1/energy-extended/system-alerts
Authorization: Bearer TOKEN

返回: 能源系统告警列表
```

### 时间窗历史数据
```
GET /api/v1/energy-extended/metrics/history/window?hours=1&granularity_minutes=1
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (可选)
- base: 基准时间 (可选)
- hours: 时间范围 (默认1)
- granularity_minutes: 粒度分钟 (默认1)

返回: 指定时间窗内的历史数据
```

---

## 5. 能源趋势模块 `/api/v1/energy-trends`

### 统一趋势查询接口
```
GET /api/v1/energy-trends/trend/{metric_type}
Authorization: Bearer TOKEN

路径参数:
- metric_type: 指标类型
  - electricity_cost: 电费趋势
  - consumption: 用电量趋势
  - green_ratio: 绿电占比趋势
  - savings: 储能节省趋势
  - co2_reduction: CO2减排趋势

查询参数:
- start_date: 开始日期 (YYYY-MM-DD, 必填)
- end_date: 结束日期 (YYYY-MM-DD, 必填)
- granularity: 时间粒度 (hour/day/week/month, 默认day)
- compare_with: 对比类型 (yoy/mom/target, 可多选)

返回:
{
  "success": true,
  "message": "趋势数据获取成功",
  "data": {
    "metric_type": "electricity_cost",
    "granularity": "day",
    "time_range": {
      "start": "2026-03-01T00:00:00+08:00",
      "end": "2026-03-20T23:59:59+08:00"
    },
    "points": [
      {"timestamp": "2026-03-01T00:00:00+08:00", "value": 5623.45, "unit": "yuan"}
    ],
    "summary": {
      "total": 112469.00,
      "average": 5623.45,
      "max": {"value": 6500.00, "timestamp": "2026-03-15T00:00:00+08:00"},
      "min": {"value": 4800.00, "timestamp": "2026-03-10T00:00:00+08:00"},
      "trend": {"direction": "up", "percentage": 5.2}
    },
    "details": {
      "cost_breakdown": {
        "grid_cost": 78728.30,
        "storage_cost": 33740.70,
        "peak_cost": 22500.00,
        "flat_cost": 56200.00,
        "valley_cost": 33769.00
      }
    },
    "comparison": {
      "mom": {"current": 5623.45, "last_month": 5400.00, "change_pct": 4.14},
      "yoy": {"current": 5623.45, "last_year": 5800.00, "change_pct": -3.05}
    }
  }
}
```

**指标与单位规则:**
| metric_type | 字段名 | 单位 | summary.total |
|-------------|--------|------|---------------|
| electricity_cost | 当日电费 | yuan | ✅ 有（累计） |
| consumption | 当日用电量 | kwh | ✅ 有（累计） |
| savings | 今日节省 | yuan | ✅ 有（累计） |
| co2_reduction | CO₂减排 | ton | ✅ 有（累计） |
| green_ratio | 绿电占比 | percent | ❌ 无（比例无意义） |

---

## 6. 绿电占比模块 `/api/v1/green-energy`

### 实时绿电占比
```
GET /api/v1/green-energy/ratio/current
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "data": {
    "ratio": 0.65,                    // 绿电占比 (0-1)
    "percentage": 65.0,               // 绿电占比百分比 (0-100)
    "load_kw": 241.5,                 // 当前负载 (kW)
    "renewable_kw": 121.0,            // 当前新能源发电 (kW)
    "bess_kw": 50.0,                  // 当前储能功率 (kW)
    "renewable_soc_ratio": 0.60,      // 储能中绿电占比 (0-1)
    "timestamp": "2026-03-20T15:30:00"
  }
}
```

### 指定日期绿电占比
```
GET /api/v1/green-energy/ratio/{date}
Authorization: Bearer TOKEN
路径参数: date (YYYY-MM-DD)

返回:
{
  "success": true,
  "data": {
    "date": "2026-03-19",
    "daily_average": 0.62,
    "average_percentage": 62.0,
    "data_points": 96,
    "min_ratio": 0.45,
    "max_ratio": 0.78,
    "std_deviation": 0.08,
    "is_simulated": false
  }
}
```

### 历史绿电占比趋势
```
GET /api/v1/green-energy/ratio/history
Authorization: Bearer TOKEN

参数:
- start_date: 开始日期 (YYYY-MM-DD, 必填)
- end_date: 结束日期 (YYYY-MM-DD, 必填)
- granularity: 时间粒度 (daily/weekly/monthly, 默认daily)

返回:
{
  "success": true,
  "data": [
    {"date": "2026-03-19", "ratio": 0.62, "percentage": 62.0},
    {"date": "2026-03-18", "ratio": 0.58, "percentage": 58.0}
  ]
}
```

### 绿电占比统计
```
GET /api/v1/green-energy/stats
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "data": {
    "total_records": 30,
    "average_ratio": 0.60,
    "average_percentage": 60.0,
    "earliest_date": "2026-02-18",
    "latest_date": "2026-03-20"
  }
}
```

---

## 7. 策略配置模块 `/api/v1/strategies`

### 获取所有策略配置
```
GET /api/v1/strategies/configs
Authorization: Bearer TOKEN

参数:
- strategy_type: 策略类型过滤 (可选)
- enabled: 启用状态过滤 (可选)

返回:
[
  {
    "id": "strategy-1",
    "name": "默认充放电策略",
    "strategy_type": "charge_discharge",
    "description": "适用于日常运行的充放电功率限制配置",
    "enabled": true,
    "priority": 8,
    "params": {
      "charge_discharge": {
        "max_charge_power": 500.0,
        "max_discharge_power": 500.0,
        "charge_efficiency_threshold": 0.90,
        "discharge_efficiency_threshold": 0.90
      }
    },
    "created_at": "2026-03-01T00:00:00",
    "updated_at": "2026-03-20T15:00:00",
    "created_by": "system",
    "last_applied": null,
    "execution_count": 0
  }
]
```

### 创建策略配置
```
POST /api/v1/strategies/configs
Authorization: Bearer TOKEN
Content-Type: application/json

请求体:
{
  "name": "削峰填谷策略",
  "strategy_type": "peak_shaving",
  "description": "策略描述",
  "enabled": true,
  "priority": 5,
  "params": {...}
}

返回: 创建的策略配置
```

### 获取/更新/删除单个策略
```
GET /api/v1/strategies/configs/{strategy_id}
PUT /api/v1/strategies/configs/{strategy_id}
DELETE /api/v1/strategies/configs/{strategy_id}
Authorization: Bearer TOKEN
```

### 切换策略状态
```
PATCH /api/v1/strategies/configs/{strategy_id}/toggle
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "message": "策略已启用/禁用",
  "data": {"id": "strategy-1", "enabled": true}
}
```

### 应用策略
```
POST /api/v1/strategies/configs/{strategy_id}/apply
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "message": "策略已应用",
  "data": {"applied_at": "2026-03-20T15:30:00"}
}
```

### 策略汇总
```
GET /api/v1/strategies/summary
Authorization: Bearer TOKEN

返回:
{
  "total_strategies": 5,
  "enabled_strategies": 3,
  "disabled_strategies": 2,
  "type_distribution": {
    "charge_discharge": 2,
    "soc_management": 1,
    "price_arbitrage": 1,
    "peak_shaving": 1
  },
  "high_priority_count": 2,
  "recently_modified": [...]
}
```

---

## 8. 调度策略模块 `/api/v1/strategy`

### 调度状态
```
GET /api/v1/strategy/status
Authorization: Bearer TOKEN

返回:
{
  "status": "running",
  "current_strategy": "智能优化调度",
  "optimization_mode": "cost_priority",
  "last_update": "2026-03-20T15:30:00"
}
```

### 调度概览
```
GET /api/v1/strategy/overview
Authorization: Bearer TOKEN

返回:
{
  "active_strategy": "智能优化调度",
  "optimization_targets": ["cost", "green_ratio", "efficiency"],
  "current_performance": {
    "cost_savings": 15.2,
    "green_ratio_improvement": 8.5,
    "efficiency_score": 92.3
  },
  "next_scheduled_action": {
    "type": "charge",
    "scheduled_time": "22:00",
    "estimated_power_kw": 5000
  }
}
```

### 调度配置
```
GET /api/v1/strategy/config
Authorization: Bearer TOKEN

返回:
{
  "optimization_mode": "cost_priority",
  "targets": {
    "cost_weight": 0.5,
    "green_weight": 0.3,
    "efficiency_weight": 0.2
  },
  "constraints": {
    "min_soc": 0.1,
    "max_soc": 0.9,
    "max_charge_power_kw": 10000,
    "max_discharge_power_kw": 8000
  }
}
```

### 训练状态
```
GET /api/v1/strategy/training
Authorization: Bearer TOKEN

返回:
{
  "is_training": false,
  "last_training_time": "2026-03-19T22:00:00",
  "training_progress": 100,
  "model_version": "v2.3.1",
  "performance_metrics": {
    "reward_score": 0.85,
    "convergence_rate": 0.92
  }
}
```

### 调试信息
```
GET /api/v1/strategy/debug
Authorization: Bearer TOKEN

返回:
{
  "algorithm_state": {...},
  "recent_decisions": [...],
  "performance_history": [...]
}
```

---

## 9. 外部服务模块 `/api/v1/external-services`

### AI智能调度建议
```
GET /api/v1/external-services/ai-recommendations/latest
Authorization: Bearer TOKEN

返回:
{
  "timestamp": "2026-03-20T11:15:00",
  "decision_horizon": "4h",
  "actions": [
    {
      "action_type": "charge",
      "power_kw": 10000,
      "charge_source": "grid",
      "start_time": "22:00",
      "end_time": "02:00",
      "duration_minutes": 240,
      "priority": "high",
      "reason": "谷电价时段充电"
    }
  ],
  "expected_outcomes": {
    "cost_savings": 6250,
    "green_energy_ratio": 0.65,
    "co2_reduction": 1250
  },
  "confidence": 0.95,
  "explanation": "详细决策解释..."
}
```

### BESS最小化任务状态
```
GET /api/v1/external-services/bess-min-task/status
Authorization: Bearer TOKEN

返回:
{
  "enabled": true,
  "last_run": "2026-03-20T10:00:00",
  "next_run": "2026-03-20T22:00:00",
  "interval_minutes": 15,
  "status": "running"
}
```

### 启用BESS最小化任务
```
POST /api/v1/external-services/bess-min-task/enable
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "message": "BESS最小化任务已启用"
}
```

### 禁用BESS最小化任务
```
POST /api/v1/external-services/bess-min-task/disable
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "message": "BESS最小化任务已禁用"
}
```

### 调度日志
```
GET /api/v1/external-services/dispatch-logs
Authorization: Bearer TOKEN

参数:
- page: 页码 (默认1)
- page_size: 每页数量 (默认20)
- status: 执行状态 (可选)
- task_id: 任务ID (可选)
- strategy_id: 策略ID (可选)

返回:
[
  {
    "id": "log-1",
    "timestamp": "2026-03-20T15:30:00",
    "action": "charge",
    "power_kw": 5000,
    "source": "grid",
    "status": "completed",
    "duration_seconds": 3600
  }
]
```

---

## 10. Dashboard模块 `/api/v1/dashboard`

### 获取所有Dashboard配置
```
GET /api/v1/dashboard/configs
Authorization: Bearer TOKEN

返回:
[
  {
    "id": "dashboard-1",
    "name": "能源总览",
    "layout": {...},
    "widgets": [...]
  }
]
```

### 创建/更新Dashboard
```
POST /api/v1/dashboard/configs
PUT /api/v1/dashboard/configs/{dashboard_id}
Authorization: Bearer TOKEN
Content-Type: application/json

请求体: DashboardConfig JSON

返回:
{
  "id": "dashboard-1",
  "name": "能源总览",
  "description": "能源监控总览面板",
  "layout": {...},
  "widgets": [...],
  "version": "1.0",
  "generatedBy": "user",
  "createdAt": "2026-03-20T15:30:00",
  "updatedAt": "2026-03-20T15:30:00"
}
```

> **注意**: DELETE `/api/v1/dashboard/configs/{dashboard_id}` 接口未实现，暂不支持删除Dashboard配置。

### 获取单个Dashboard配置
```
GET /api/v1/dashboard/configs/{dashboard_id}
Authorization: Bearer TOKEN

返回: 单个Dashboard配置详情
```

### Dashboard KPI数据
```
GET /api/v1/dashboard/kpi
Authorization: Bearer TOKEN

返回:
{
  "total_energy_kwh": 12500.5,
  "green_ratio": 0.65,
  "cost_savings": 1500.00,
  "co2_reduction_tons": 12.5
}
```

### Dashboard 概览
```
GET /api/v1/dashboard/overview
Authorization: Bearer TOKEN

返回: 系统整体概览数据
```

### Dashboard 实时数据
```
GET /api/v1/dashboard/realtime
Authorization: Bearer TOKEN

返回: 实时监控数据
```

### Dashboard 组件列表
```
GET /api/v1/dashboard/widgets
Authorization: Bearer TOKEN

返回: 可用的Dashboard组件/小部件列表
```

---

## 11. 集群模块 `/api/v1/cluster`

> **重要说明**: 本模块基于 pp-sim 外部服务，以下写操作接口返回"pp-sim不支持"：
> - `PUT /pdu/{pdu_id}` - 更新PDU配置
> - `PUT /cooling/{unit_id}` - 更新制冷单元配置
> - `PUT /lighting/{zone_id}` - 更新照明区域配置
> - `POST /lighting/{zone_id}/toggle` - 切换照明状态
> - `PUT /config/cabinet/{cabinet_id}` - 更新机柜配置
> - `POST /config/cabinet/batch` - 批量更新机柜配置
> - `POST /alerts/acknowledge/{alert_id}` - 确认告警
> - `POST /alerts/close/{alert_id}` - 关闭告警
> - `POST /reports/generate` - 生成报告
> - `POST /cabinets/batch/delete` - 批量删除机柜
> - `POST /cabinets/batch/update-status` - 批量更新机柜状态
> - `POST /pdus/batch/restart` - 批量重启PDU
> - `POST /cooling/batch/set-setpoint` - 批量设置制冷温度
>
> 这些接口返回格式: `{"success": false, "message": "pp-sim 不支持"}`

### 集群概览
```
GET /api/v1/cluster/overview
Authorization: Bearer TOKEN

返回:
{
  "total_power": 250.5,
  "total_energy": 6000.0,
  "pdu_load_avg": 65.5,
  "online_cabinets": 10,
  "total_cabinets": 12,
  "normal_cabinets": 8,
  "warning_cabinets": 2,
  "alarm_cabinets": 0,
  "timestamp": "2026-03-20T15:30:00"
}
```

### 功率曲线
```
GET /api/v1/cluster/power-curve?hours=24
Authorization: Bearer TOKEN

返回:
[
  {"time": "2026-03-20T14:00:00", "power": 250.5}
]
```

### 机柜列表
```
GET /api/v1/cluster/cabinets
Authorization: Bearer TOKEN

参数:
- zone: 区域 (可选)
- row: 行 (可选)
- status: 状态 (可选)

返回:
[
  {
    "id": "cabinet-1",
    "name": "机柜-1",
    "location": {"row": "A", "column": 1, "zone": "zone-1"},
    "type": "compute",
    "status": "normal",
    "current_power": 25.5,
    "pdu_load": 65.5,
    "temperature": 28.5
  }
]
```

### 机柜详情
```
GET /api/v1/cluster/cabinet/{cabinet_id}
Authorization: Bearer TOKEN

返回: 机柜详细信息
```

### 告警列表
```
GET /api/v1/cluster/alerts?level=warning&limit=50
Authorization: Bearer TOKEN

返回:
[
  {
    "id": "alert-1",
    "cabinet_id": "cabinet-1",
    "level": "warning",
    "message": "温度偏高",
    "timestamp": "2026-03-20T15:30:00"
  }
]
```

---

## 12. 算力模块 `/api/v1/compute`

### 实时算力数据
```
GET /api/v1/compute/realtime
Authorization: Bearer TOKEN

返回:
{
  "timestamp": "2026-03-20T15:30:00",
  "gpu_utilization": 75.5,
  "gpu_temperature": 68.2,
  "active_tasks": 25,
  "queue_length": 10,
  "cluster_health": 0.95,
  "memory_usage": 80.2,
  "power_consumption": 350.5,
  "total_nodes": 10,
  "total_tasks": 35,
  "data_source": "bmc_real"
}
```

### 节点列表
```
GET /api/v1/compute/nodes
Authorization: Bearer TOKEN

返回:
[
  {
    "id": "node-1",
    "name": "计算节点-1",
    "status": "Ready",
    "gpu_total": 8,
    "gpu_used": 6,
    "memory_total": 256,
    "memory_used": 200,
    "temperature": 68.5
  }
]
```

### 任务队列
```
GET /api/v1/compute/queue
Authorization: Bearer TOKEN

返回:
{
  "pending_tasks": 10,
  "running_tasks": 25,
  "completed_tasks_today": 50,
  "avg_wait_time": 120.5,
  "queue_utilization": 75.5,
  "tasks": [...]
}
```

### 集群拓扑
```
GET /api/v1/compute/topology
Authorization: Bearer TOKEN

返回:
{
  "nodes": [...],
  "pods": [...],
  "connections": [...]
}
```

### 集群功率（实时）
```
GET /api/v1/compute/cluster/power/realtime?source=simulated
Authorization: Bearer TOKEN

参数:
- source: 数据源 (simulated/prom)

返回:
{
  "timestamp": "2026-03-20T15:30:00",
  "power_kw": 350.5,
  "power_mw": 0.35,
  "cpu_cores": 128,
  "gpu_count": 80,
  "jobs_running": 25,
  "source": "simulated"
}
```

### 集群功率历史
```
GET /api/v1/compute/cluster/power/history?hours=24&step_minutes=5
Authorization: Bearer TOKEN

参数:
- hours: 时间范围 (1-168, 默认24)
- step_minutes: 步进分钟 (1-60, 默认5)
- source: 数据源 (simulated/prom)

返回:
{
  "hours": 24,
  "step_minutes": 5,
  "source": "simulated",
  "data": [
    {"timestamp": "2026-03-20T14:00:00", "power_kw": 350.5}
  ]
}
```

### 集群功率时间窗历史
```
GET /api/v1/compute/cluster/power/history/window?hours=1&granularity_minutes=1
Authorization: Bearer TOKEN

参数:
- hours: 时间范围 (1-168, 默认1)
- granularity_minutes: 粒度 (1-60, 默认1)
- base: 基准时间 (可选, 格式: YYYY-MM-DD HH:MM:SS)
- source: 数据源 (simulated/prom)

返回:
{
  "hours": 1,
  "granularity_minutes": 1,
  "base": null,
  "source": "simulated",
  "data": [
    {"timestamp": "2026-03-20T15:00:00", "power_kw": 350.5}
  ]
}
```

### 算力历史数据
```
GET /api/v1/compute/history?minutes=1440
Authorization: Bearer TOKEN

参数:
- minutes: 时间范围 (分钟, 默认1440)
- granularity: 粒度 (可选)

返回:
[
  {
    "timestamp": "2026-03-20T14:00:00",
    "gpu_utilization": 75.5,
    "gpu_temperature": 68.2,
    "active_tasks": 25,
    "queue_length": 10,
    "cluster_health": 0.95,
    "memory_usage": 80.2,
    "power_consumption": 350.5,
    "total_nodes": 10,
    "total_tasks": 35
  }
]
```

### BMC硬件监控数据
```
GET /api/v1/compute/bmc/hardware
Authorization: Bearer TOKEN

返回:
{
  "timestamp": "2026-03-20T15:30:00",
  "data_source": "prometheus_bmc",
  "cluster_summary": {
    "total_nodes": 10,
    "active_gpus": 80,
    "total_power_consumption": 350.5,
    "average_gpu_utilization": 75.5,
    "average_memory_utilization": 80.2,
    "cluster_health": 0.95
  },
  "available": true,
  "nodes_count": 10,
  "active_gpus": 80,
  "total_power_consumption": 350.5
}
```

### BMC增强节点信息
```
GET /api/v1/compute/bmc/nodes
Authorization: Bearer TOKEN

返回:
{
  "timestamp": "2026-03-20T15:30:00",
  "data_source": "enhanced_bmc",
  "nodes": [
    {
      "id": "node-1",
      "name": "计算节点-1",
      "status": "Ready",
      "gpu_total": 8,
      "gpu_used": 6,
      "memory_total": 256,
      "memory_used": 200,
      "temperature": 68.5,
      "bmc_data": {...}
    }
  ],
  "total_nodes": 10
}
```

---

## 13. ESG模块 `/api/v1/esg`

### ESG概要
```
GET /api/v1/esg/summary?days=30
Authorization: Bearer TOKEN

参数:
- days: 天数 (1-365, 默认30)

返回:
{
  "total_co2_reduction": 12500.0,    // 总CO2减排量 (吨)
  "avg_green_energy_ratio": 0.65,    // 平均绿电占比
  "total_carbon_credits": 18750.0,   // 总碳信用
  "current_efficiency": 0.80,        // 当前能效
  "co2_reduction_trend_pct": 5.2,    // CO2减排趋势 (%)
  "period_start": "2026-03-01T00:00:00",
  "period_end": "2026-03-20T23:59:59",
  "last_updated": "2026-03-20T15:30:00",
  "unit": "tCO2e",
  "data_source": "ppsim_real"
}
```

### ESG趋势
```
GET /api/v1/esg/trends?days=30
Authorization: Bearer TOKEN

参数:
- days: 天数 (1-365, 默认30)

返回:
[
  {
    "timestamp": "2026-03-20T00:00:00",
    "co2_reduction": 125.5,
    "green_energy_ratio": 0.65,
    "energy_efficiency": 0.80,
    "carbon_credits": 188.25
  }
]
```

### ESG趋势（单条）
```
GET /api/v1/esg/trend?days=30
Authorization: Bearer TOKEN

参数:
- days: 天数 (1-365, 默认30)

返回: ESG趋势汇总数据（与/trends类似，返回格式可能略有不同）
```

### 碳资产管理
```
GET /api/v1/esg/carbon
Authorization: Bearer TOKEN

返回:
{
  "total_credits": 500.0,
  "available_credits": 350.0,
  "used_credits": 150.0,
  "credit_value": 45.50,
  "transactions": [
    {
      "id": "txn-202603-1",
      "type": "购买",
      "amount": 25.0,
      "date": "2026-03-15T10:00:00",
      "counterparty": "企业1"
    }
  ]
}
```

### ESG报告列表
```
GET /api/v1/esg/reports
Authorization: Bearer TOKEN

返回:
{
  "reports": [
    {
      "id": "report-1",
      "period": "2024-Q3",
      "status": "completed",
      "created_at": "2024-10-01T00:00:00",
      "download_url": "/api/v1/esg/reports/report-1/download"
    }
  ],
  "total_reports": 1
}
```

---

## 14. 告警模块 `/api/v1/alerts`

### 告警面板
```
GET /api/v1/alerts/panel
Authorization: Bearer TOKEN

返回:
{
  "total_alerts": 15,
  "critical_count": 2,
  "warning_count": 8,
  "info_count": 5,
  "recent_alerts": [...]
}
```

### 告警列表
```
GET /api/v1/alerts
Authorization: Bearer TOKEN

参数:
- level: 告警级别过滤 (可选)
- limit: 数量限制 (默认50)
- offset: 偏移量 (默认0)

返回:
[
  {
    "id": "alert-1",
    "level": "warning",
    "source": "cluster",
    "message": "机柜温度偏高",
    "timestamp": "2026-03-20T15:30:00",
    "acknowledged": false
  }
]
```

### 告警规则列表
```
GET /api/v1/alerts/rules
Authorization: Bearer TOKEN

返回:
[
  {
    "id": "rule-1",
    "name": "温度告警规则",
    "category": "temperature",
    "metric_name": "cpu_temperature",
    "condition": "greater_than",
    "severity": "warning",
    "threshold": 35.0,
    "enabled": true,
    "notification_channels": ["email", "sms"],
    "notification_interval": 300,
    "cooldown_period": 600,
    "created_at": "2026-03-01T00:00:00Z",
    "updated_at": "2026-03-20T15:00:00Z"
  }
]
```

### 创建告警规则
```
POST /api/v1/alerts/rules
Authorization: Bearer TOKEN
Content-Type: application/json

请求体:
{
  "name": "温度告警规则",
  "category": "temperature",
  "metric_name": "cpu_temperature",
  "condition": "greater_than",
  "severity": "warning",
  "threshold": 35.0,
  "enabled": true,
  "notification_channels": ["email", "sms"]
}

返回: 创建的规则
```

### 更新告警规则
```
PUT /api/v1/alerts/rules/{rule_id}
Authorization: Bearer TOKEN
Content-Type: application/json

请求体: 规则更新字段

返回: 更新后的规则
```

### 删除告警规则
```
DELETE /api/v1/alerts/rules/{rule_id}
Authorization: Bearer TOKEN

返回: { "success": true }
```

### 切换规则状态
```
PATCH /api/v1/alerts/rules/{rule_id}/toggle
Authorization: Bearer TOKEN

请求体:
{
  "enabled": true
}

返回: 更新后的规则
```

### 规则汇总
```
GET /api/v1/alerts/rules/summary
Authorization: Bearer TOKEN

返回:
{
  "total_rules": 10,
  "enabled_count": 8,
  "by_type": {
    "temperature": 3,
    "power": 4,
    "network": 3
  }
}
```

### 系统日志
```
GET /api/v1/alerts/logs
Authorization: Bearer TOKEN

参数:
- level: 日志级别 (可选)
- source: 来源 (可选)
- start_time: 开始时间 (可选)
- end_time: 结束时间 (可选)
- limit: 数量限制 (默认100)

返回: 系统日志列表
```

---

## 15. 智能代理模块 `/api/v1/agents`

> **返回格式说明**: 所有接口返回统一包装格式：
> ```json
> {
>   "success": true,
>   "message": "ok",
>   "data": { /* 实际数据 */ }
> }
> ```

### 发送消息
```
POST /api/v1/agents/chat
Authorization: Bearer TOKEN
Content-Type: application/json

请求体:
{
  "message": "今天储能状态怎么样？",
  "session_id": "admin:abc123"  // 可选
}

返回:
{
  "success": true,
  "message": "ok",
  "data": {
    "session_id": "admin:abc123",
    "message": {
      "id": "msg-1",
      "role": "assistant",
      "content": "当前储能SOC为65%...",
      "timestamp": "2026-03-20T15:30:00"
    }
  }
}
```

### 流式消息
```
POST /api/v1/agents/chat/stream
Authorization: Bearer TOKEN
Content-Type: application/json

请求体: 同上

返回: SSE事件流
event: status
data: {"type": "status", "text": "已接收消息..."}

event: tool_start
data: {"type": "tool_start", "tool": "exec", "text": "正在调用工具..."}

event: final
data: {"type": "final", "session_id": "...", "message": {...}}
```

### 会话列表
```
GET /api/v1/agents/sessions?limit=20&offset=0
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "message": "ok",
  "data": {
    "sessions": [
      {
        "id": "admin:abc123",
        "title": "储能状态查询",
        "last_message": "...",
        "updated_at": "2026-03-20T15:30:00",
        "message_count": 5
      }
    ],
    "total": 10
  }
}
```

### 会话消息
```
GET /api/v1/agents/sessions/{session_id}/messages?limit=50
Authorization: Bearer TOKEN

返回: 消息列表
```

### 重命名会话
```
PATCH /api/v1/agents/sessions/{session_id}
Authorization: Bearer TOKEN
Content-Type: application/json

请求体:
{
  "title": "新会话标题"
}

返回:
{
  "success": true,
  "message": "ok",
  "data": {
    "id": "admin:abc123",
    "title": "新会话标题",
    "updated_at": "2026-03-20T15:30:00"
  }
}
```

### 删除会话
```
DELETE /api/v1/agents/sessions/{session_id}
Authorization: Bearer TOKEN

返回:
{
  "success": true,
  "message": "ok",
  "data": {"deleted": true}
}
```

---

## 16. PP-Sim模块 `/api/v1/pp-sim`

PP-Sim是外部电力价格模拟服务代理模块，提供丰富的电力系统模拟数据。

### 集群负载状态
```
GET /api/v1/pp-sim/cluster-load/status
Authorization: Bearer TOKEN

返回:
{
  "simulators": [
    {
      "id": "cluster-sim-1",
      "name": "主集群负载模拟器",
      "status": "running",
      "load_kw": 350.5
    }
  ]
}
```

### 集群负载最新数据
```
GET /api/v1/pp-sim/cluster-load/{simulator_id}/latest
Authorization: Bearer TOKEN

返回:
{
  "simulator_id": "cluster-sim-1",
  "timestamp": "2026-03-20T15:30:00",
  "load_kw": 350.5,
  "load_mw": 0.35
}
```

### 集群负载每日数据
```
GET /api/v1/pp-sim/cluster-load/{simulator_id}/daily
Authorization: Bearer TOKEN

参数:
- date: 日期 (YYYY-MM-DD, 可选)

返回:
{
  "date": "2026-03-20",
  "avg_load_kw": 320.5,
  "peak_load_kw": 450.0,
  "min_load_kw": 180.0,
  "total_energy_kwh": 7680.0
}
```

### 集群负载历史序列
```
GET /api/v1/pp-sim/cluster-load/{simulator_id}/load-series
Authorization: Bearer TOKEN

参数:
- start: 开始时间 (ISO格式)
- end: 结束时间 (ISO格式)
- step_minutes: 步进分钟数 (默认5)
- tz: 时区 (默认Asia/Shanghai)

返回:
{
  "series": [
    {"timestamp": "2026-03-20T15:00:00", "load_kw": 350.5}
  ]
}
```

### 机柜列表
```
GET /api/v1/pp-sim/cabinets
Authorization: Bearer TOKEN

返回:
[
  {
    "id": "cabinet-1",
    "name": "机柜-1",
    "location": {"row": "A", "column": 1, "zone": "zone-1"},
    "type": "compute",
    "status": "normal",
    "current_power": 25.5,
    "pdu_load": 65.5,
    "temperature": 28.5
  }
]
```

### 机柜详情
```
GET /api/v1/pp-sim/cabinets/{cabinet_id}
Authorization: Bearer TOKEN

返回: 机柜详细信息
```

### 制冷系统列表
```
GET /api/v1/pp-sim/cooling
Authorization: Bearer TOKEN

返回:
[
  {
    "id": "cooling-1",
    "name": "精密空调-1",
    "type": "precision",
    "location": "zone-1",
    "status": "running",
    "supply_temp": 18.5,
    "return_temp": 28.0,
    "power": 45.5
  }
]
```

### 制冷系统详情
```
GET /api/v1/pp-sim/cooling/{unit_id}
Authorization: Bearer TOKEN

返回: 制冷系统详细信息
```

### 照明系统列表
```
GET /api/v1/pp-sim/lighting
Authorization: Bearer TOKEN

返回:
[
  {
    "id": "lighting-1",
    "name": "照明区域-1",
    "location": "zone-1",
    "status": "on",
    "brightness": 80.0,
    "power": 2.5
  }
]
```

### 照明系统详情
```
GET /api/v1/pp-sim/lighting/{zone_id}
Authorization: Bearer TOKEN

返回: 照明系统详细信息
```

### 配电系统状态
```
GET /api/v1/pp-sim/power-distribution
Authorization: Bearer TOKEN

返回:
{
  "main_switch_status": "on",
  "total_power_kw": 500.0,
  "circuits": [...]
}
```

### 站点列表
```
GET /api/v1/pp-sim/sites
Authorization: Bearer TOKEN

返回:
[
  {
    "id": "shanghai_jiading",
    "name": "上海嘉定数据中心",
    "location": "上海市嘉定区",
    "status": "operational",
    "capacity_mw": 10.0
  }
]
```

### 站点详情
```
GET /api/v1/pp-sim/sites/{site_id}
Authorization: Bearer TOKEN

返回: 站点详细信息
```

### 发电机组指标
```
GET /api/v1/pp-sim/generators/site/metrics/latest
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (可选)

返回:
{
  "total_capacity_kw": 5000.0,
  "active_generators": 3,
  "total_output_kw": 2500.0,
  "fuel_consumption_rate": 150.5
}
```

### 当前电价
```
GET /api/v1/pp-sim/pricing/current
Authorization: Bearer TOKEN

返回:
{
  "timestamp": "2026-03-20T15:30:00",
  "price_type": "peak",
  "tou_price": 0.85,
  "spot_price": 0.82,
  "contract_price": 0.45
}
```

### 电价预测
```
GET /api/v1/pp-sim/pricing/forecast?hours=24
Authorization: Bearer TOKEN

返回:
[
  {
    "timestamp": "2026-03-20T16:00:00",
    "price_type": "normal",
    "tou_price": 0.65
  }
]
```

### 储能系统状态
```
GET /api/v1/pp-sim/bess/status
Authorization: Bearer TOKEN

返回:
{
  "soc": 65.5,
  "charge_power": 0.0,
  "discharge_power": 50.0,
  "capacity_kwh": 20000.0,
  "available_capacity_kwh": 13100.0,
  "status": "discharging"
}
```

### 储能调度计划
```
GET /api/v1/pp-sim/bess/schedule
Authorization: Bearer TOKEN

返回:
{
  "site_id": "shanghai_jiading",
  "schedule": [
    {
      "start_time": "22:00",
      "end_time": "06:00",
      "action": "charge",
      "power_kw": 5000,
      "status": "scheduled"
    }
  ]
}
```

### 指标历史数据
```
GET /api/v1/pp-sim/metrics/history?hours=24
Authorization: Bearer TOKEN

返回:
{
  "metrics": [
    {
      "timestamp": "2026-03-20T15:00:00",
      "total_power_kw": 500.5,
      "avg_temperature": 25.5,
      "pue": 1.35
    }
  ]
}
```

### 预测模拟
```
POST /api/v1/predict-simulation/generate
Authorization: Bearer TOKEN
Content-Type: application/json

请求体: 模拟参数

返回: 预测模拟结果
```

---

## 17. PP-Sim模块 `/api/v1/pp-sim` (完整版)

PP-Sim是外部电力价格模拟服务代理模块，提供丰富的电力系统模拟数据。

### 17.1 集群负载子模块

#### 集群负载状态
```
GET /api/v1/pp-sim/cluster-load/status
Authorization: Bearer TOKEN

返回:
{
  "simulators": [
    {
      "id": "cluster-sim-1",
      "name": "主集群负载模拟器",
      "status": "running",
      "load_kw": 350.5
    }
  ],
  "total_load_kw": 350.5
}
```

#### 集群负载最新数据
```
GET /api/v1/pp-sim/cluster-load/{simulator_id}/latest
Authorization: Bearer TOKEN

返回:
{
  "simulator_id": "cluster-sim-1",
  "timestamp": "2026-03-20T15:30:00",
  "load_kw": 350.5,
  "load_mw": 0.35,
  "total_cpu_cores": 128,
  "total_gpu": 80,
  "jobs_summary": {"running": 25, "pending": 10}
}
```

#### 集群负载每日数据
```
GET /api/v1/pp-sim/cluster-load/{simulator_id}/daily
Authorization: Bearer TOKEN

参数:
- date: 日期 (YYYY-MM-DD, 可选, 默认今天)
- tz: 时区 (默认Asia/Shanghai)

返回:
{
  "date": "2026-03-20",
  "avg_load_kw": 320.5,
  "peak_load_kw": 450.0,
  "min_load_kw": 180.0,
  "total_energy_kwh": 7680.0
}
```

#### 集群负载历史序列
```
GET /api/v1/pp-sim/cluster-load/{simulator_id}/load-series
Authorization: Bearer TOKEN

参数:
- start: 开始时间 (ISO格式, 必填)
- end: 结束时间 (ISO格式, 必填)
- step_minutes: 步进分钟数 (默认5)
- tz: 时区 (默认Asia/Shanghai)

返回:
{
  "series": [
    {"timestamp": "2026-03-20T15:00:00", "load_kw": 350.5}
  ]
}
```

#### 集群负载历史记录
```
GET /api/v1/pp-sim/cluster-load/{simulator_id}/history
Authorization: Bearer TOKEN

参数:
- start: 开始时间 (可选)
- end: 结束时间 (可选)
- limit: 数量 (默认100)
- step_minutes: 步进分钟数 (默认5)

返回: 历史负载数据列表
```

#### 峰值占比检查
```
GET /api/v1/pp-sim/cluster-load/{simulator_id}/peak-check
Authorization: Bearer TOKEN

参数:
- date: 日期 (YYYY-MM-DD, 可选)

返回:
{
  "date": "2026-03-20",
  "peak_ratio": 0.75,
  "is_compliant": true,
  "threshold": 0.80
}
```

### 17.2 机柜子模块

#### 机柜列表
```
GET /api/v1/pp-sim/cabinets
Authorization: Bearer TOKEN

参数:
- simulator_id: 模拟器ID (可选)
- offset: 偏移量 (默认0)
- limit: 数量 (默认100)

返回:
[
  {
    "id": "cabinet-1",
    "name": "机柜-1",
    "location": {"row": "A", "column": 1, "zone": "zone-1"},
    "type": "compute",
    "status": "normal",
    "current_power": 25.5,
    "pdu_load": 65.5,
    "temperature": 28.5
  }
]
```

#### 机柜详情
```
GET /api/v1/pp-sim/cabinets/{cabinet_id}
Authorization: Bearer TOKEN

参数:
- simulator_id: 模拟器ID (可选)

返回: 机柜详细信息
```

#### 机柜实时指标
```
GET /api/v1/pp-sim/cabinets/{cabinet_id}/metrics/latest
Authorization: Bearer TOKEN

参数:
- simulator_id: 模拟器ID (可选)

返回:
{
  "cabinet_id": "cabinet-1",
  "timestamp": "2026-03-20T15:30:00",
  "power_kw": 25.5,
  "temperature": 28.5,
  "pdu_load": 65.5
}
```

#### 机柜秒级指标序列
```
GET /api/v1/pp-sim/cabinets/{cabinet_id}/metrics/series-seconds
Authorization: Bearer TOKEN

参数:
- simulator_id: 模拟器ID (可选)
- start: 开始时间 (必填)
- end: 结束时间 (必填)
- step_seconds: 步进秒数 (默认60)
- tz: 时区 (可选)

返回:
{
  "series": [
    {"timestamp": "2026-03-20T15:00:00", "power_kw": 25.5}
  ]
}
```

### 17.3 制冷/照明/配电子模块

#### 制冷设备列表
```
GET /api/v1/pp-sim/cooling
Authorization: Bearer TOKEN

参数:
- simulator_id: 模拟器ID (可选)
- offset: 偏移量 (默认0)
- limit: 数量 (默认100)

返回:
[
  {
    "id": "cooling-1",
    "name": "精密空调-1",
    "type": "precision",
    "location": "zone-1",
    "status": "running",
    "supply_temp": 18.5,
    "return_temp": 28.0,
    "power": 45.5
  }
]
```

#### 制冷设备详情
```
GET /api/v1/pp-sim/cooling/{device_id}
Authorization: Bearer TOKEN

参数:
- simulator_id: 模拟器ID (可选)

返回: 制冷设备详细信息
```

#### 制冷设备实时指标
```
GET /api/v1/pp-sim/cooling/{device_id}/metrics/latest
Authorization: Bearer TOKEN

参数:
- simulator_id: 模拟器ID (可选)

返回: 制冷设备实时指标
```

#### 照明设备列表/详情/指标
```
GET /api/v1/pp-sim/lighting
GET /api/v1/pp-sim/lighting/{device_id}
GET /api/v1/pp-sim/lighting/{device_id}/metrics/latest
Authorization: Bearer TOKEN

参数:
- simulator_id: 模拟器ID (可选)

返回: 照明设备信息
```

#### 配电设备列表/详情/指标
```
GET /api/v1/pp-sim/power-distribution
GET /api/v1/pp-sim/power-distribution/{device_id}
GET /api/v1/pp-sim/power-distribution/{device_id}/metrics/latest
Authorization: Bearer TOKEN

参数:
- simulator_id: 模拟器ID (可选)

返回: 配电设备信息
```

### 17.4 站点与发电机组

#### 站点列表
```
GET /api/v1/pp-sim/sites/
Authorization: Bearer TOKEN

返回:
[
  {
    "id": "shanghai_jiading",
    "name": "上海嘉定数据中心",
    "location": "上海市嘉定区",
    "status": "operational",
    "capacity_mw": 10.0
  }
]
```

#### 站点详情
```
GET /api/v1/pp-sim/sites/{site_id}/
Authorization: Bearer TOKEN

返回: 站点详细信息
```

#### 发电机组站点指标
```
GET /api/v1/pp-sim/generators/site/metrics/latest
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (可选)

返回:
{
  "pv_power_kw": 250.0,
  "wind_power_kw": 150.0,
  "bess_power_kw": 50.0,
  "bess_soc": 65.5,
  "e_day_kwh": 1250.0
}
```

#### 指定类型发电机组指标
```
GET /api/v1/pp-sim/generators/{generator}/site/metrics/latest
GET /api/v1/pp-sim/generators/{generator}/metrics/latest
Authorization: Bearer TOKEN

路径参数:
- generator: 发电机类型 (pv/bess等)

参数:
- site_id: 站点ID (可选)

返回: 发电机组指标
```

### 17.5 电价模块

#### 当前电价
```
GET /api/v1/pp-sim/pricing/current
Authorization: Bearer TOKEN

参数:
- city: 城市名 (必填)
- price_type: 价格类型 (默认grid_buy)
- timestamp: 时间戳 (可选)

返回:
{
  "timestamp": "2026-03-20T15:30:00",
  "price_type": "peak",
  "tou_price": 0.85,
  "spot_price": 0.82,
  "contract_price": 0.45
}
```

#### 站点新能源价格
```
GET /api/v1/pp-sim/pricing/site-renewable-price
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (必填)
- time: 时间 (可选)

返回:
{
  "site_id": "shanghai_jiading",
  "renewable_price": 0.45,
  "timestamp": "2026-03-20T15:30:00"
}
```

#### 批量电价查询
```
GET /api/v1/pp-sim/pricing/batch
Authorization: Bearer TOKEN

参数:
- city: 城市名 (必填)
- start_time: 开始时间 (必填)
- end_time: 结束时间 (必填)
- price_type: 价格类型 (默认grid_buy)

返回: 时间段内电价列表
```

#### 电价预测
```
GET /api/v1/pp-sim/pricing/forecast
Authorization: Bearer TOKEN

参数:
- city: 城市名 (必填)
- days_ahead: 预测天数 (1-30, 默认1)
- price_type: 价格类型 (默认grid_buy)

返回:
[
  {
    "timestamp": "2026-03-20T16:00:00",
    "price_type": "normal",
    "tou_price": 0.65
  }
]
```

#### 每日加权电价
```
GET /api/v1/pp-sim/pricing/weighted/day
Authorization: Bearer TOKEN

参数:
- date: 日期 (可选, 默认今天)
- site_id: 站点ID (可选)
- granularity_seconds: 粒度秒数 (默认60)

返回: 每日加权电价数据
```

#### 电价统计
```
GET /api/v1/pp-sim/pricing/statistics
Authorization: Bearer TOKEN

参数:
- city: 城市名 (必填)
- period: 时间周期 (必填)

返回: 电价统计信息
```

#### 电价模板
```
GET /api/v1/pp-sim/pricing/templates/{city}/{year}
Authorization: Bearer TOKEN

路径参数:
- city: 城市名
- year: 年份

返回:
{
  "city": "shanghai",
  "year": 2026,
  "peak_price": 1.2,
  "normal_price": 0.8,
  "valley_price": 0.3,
  "deep_valley_price": 0.2
}
```

### 17.6 储能系统 (BESS)

#### 储能放电价格
```
GET /api/v1/pp-sim/bess/discharge-price
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (可选)

返回:
{
  "discharge_price": 0.65,
  "charge_cost": 0.35,
  "profit_margin": 0.30
}
```

#### 储能状态汇总
```
GET /api/v1/pp-sim/sites/bess/status/summary/
Authorization: Bearer TOKEN

返回:
{
  "sites": {
    "shanghai_jiading": {
      "soc": 65.5,
      "status": "discharging",
      "power_kw": 50.0
    }
  }
}
```

#### 站点历史数据
```
GET /api/v1/pp-sim/metrics/history
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (必填)
- date: 日期 (可选)

返回:
{
  "points": [
    {"timestamp": "2026-03-20T15:00:00", "pv_power_kw": 250.0, "bess_power_kw": 50.0}
  ]
}
```

#### 时间窗功率历史
```
GET /api/v1/pp-sim/metrics/history/window
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (可选)
- base: 基准时间 (可选)
- hours: 时间窗 (1-168, 默认1)
- granularity_minutes: 粒度分钟 (1-60, 默认1)

返回:
{
  "points": [
    {"timestamp": "2026-03-20T15:00:00", "pv_power_kw": 250.0, "bess_power_kw": 50.0, "total_power_kw": 300.0}
  ]
}
```

#### 秒级时间窗历史
```
GET /api/v1/pp-sim/metrics/history/window/seconds
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (可选)
- start_time: 开始时间 (可选)
- end_time: 结束时间 (可选)
- base: 基准时间 (可选)
- hours: 时间窗 (1-168, 默认1)
- granularity_seconds: 粒度秒数 (1-60, 默认1)

返回: 秒级历史数据
```

#### 储能经济分析
```
GET /api/v1/pp-sim/sites/bess/{site_id}/economic-analysis
Authorization: Bearer TOKEN

参数:
- period: 时间周期 (可选)

返回:
{
  "site_id": "shanghai_jiading",
  "total_revenue": 15000.0,
  "total_cost": 8000.0,
  "net_profit": 7000.0,
  "roi": 0.15
}
```

#### 储能容量数据
```
GET /api/v1/pp-sim/bess/capacity/data
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (可选)
- hours: 时间范围 (1-168, 默认24)

返回:
{
  "success": true,
  "data": {
    "series": [
      {"metric": "soc", "data": [{"x": "timestamp", "y": 0.65}]},
      {"metric": "power", "data": [{"x": "timestamp", "y": 50.0}]}
    ]
  }
}
```

### 17.7 储能配置管理

#### 获取储能约束配置
```
GET /api/v1/pp-sim/bess/constraints
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (必填)

返回:
{
  "site_id": "shanghai_jiading",
  "soc_min": 0.1,
  "soc_max": 0.95,
  "max_charge_kw": 10000,
  "max_discharge_kw": 8000,
  "ramp_rate_kw_per_min": 500,
  "ramp_to_max_seconds": 60
}
```

#### 更新储能约束配置
```
POST /api/v1/pp-sim/bess/constraints
Authorization: Bearer TOKEN
Content-Type: application/json

请求体:
{
  "site_id": "shanghai_jiading",
  "soc_min": 0.1,
  "soc_max": 0.95,
  "max_charge_kw": 10000,
  "max_discharge_kw": 8000,
  "ramp_rate_kw_per_min": 500
}

返回: 更新后的配置
```

#### 自动光伏充电状态
```
GET /api/v1/pp-sim/bess/auto-photovoltaic-charge/status
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (必填)

返回:
{
  "site_id": "shanghai_jiading",
  "enabled": true,
  "status": "running"
}
```

#### 启用/禁用自动光伏充电
```
POST /api/v1/pp-sim/bess/auto-photovoltaic-charge/enable
POST /api/v1/pp-sim/bess/auto-photovoltaic-charge/disable
Authorization: Bearer TOKEN
Content-Type: application/json

请求体:
{
  "site_id": "shanghai_jiading"
}

返回:
{
  "success": true,
  "message": "操作成功"
}
```

#### 实时负载响应状态
```
GET /api/v1/pp-sim/bess/realtime-load-response/status
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (必填)

返回:
{
  "site_id": "shanghai_jiading",
  "enabled": true,
  "status": "running"
}
```

#### 启用/禁用实时负载响应
```
POST /api/v1/pp-sim/bess/realtime-load-response/enable
POST /api/v1/pp-sim/bess/realtime-load-response/disable
Authorization: Bearer TOKEN
Content-Type: application/json

请求体:
{
  "site_id": "shanghai_jiading"
}

返回:
{
  "success": true,
  "message": "操作成功"
}
```

#### 自适应充放电状态
```
GET /api/v1/pp-sim/bess/adaptive-charge-discharge/status
Authorization: Bearer TOKEN

参数:
- site_id: 站点ID (必填)

返回:
{
  "site_id": "shanghai_jiading",
  "enabled": true,
  "status": "running"
}
```

#### 启用/禁用自适应充放电
```
POST /api/v1/pp-sim/bess/adaptive-charge-discharge/enable
POST /api/v1/pp-sim/bess/adaptive-charge-discharge/disable
Authorization: Bearer TOKEN
Content-Type: application/json

请求体:
{
  "site_id": "shanghai_jiading"
}

返回:
{
  "success": true,
  "message": "操作成功"
}
```

### 17.8 预测仿真子模块 `/api/v1/predict-simulation`

> **说明**: 此子模块用于运行储能调度策略的仿真预测。
> **注意**: 路径为 `/api/v1/predict-simulation`（不是 `/api/v1/pp-sim/predict-simulation`）

#### 查询仿真记录
```
GET /api/v1/predict-simulation/records
Authorization: Bearer TOKEN

参数:
- page: 页码 (默认1)
- page_size: 每页数量 (默认20)

返回: 仿真记录列表
```

#### 创建仿真记录
```
POST /api/v1/predict-simulation/records
Authorization: Bearer TOKEN
Content-Type: application/json

请求体:
{
  "run_uuid": "uuid-string",
  "run_type": "forecast",
  "start_time": "2026-03-20T00:00:00",
  "end_time": "2026-03-21T00:00:00"
}

返回: 创建的仿真记录
```

#### 查询仿真步骤
```
GET /api/v1/predict-simulation/steps
Authorization: Bearer TOKEN

参数:
- simulation_uuid: 仿真UUID (必填)

返回: 仿真步骤详情列表
```

#### 批量创建仿真步骤
```
POST /api/v1/predict-simulation/steps/batch
Authorization: Bearer TOKEN
Content-Type: application/json

请求体: 仿真步骤数组

返回: 创建结果
```

#### 生成仿真
```
POST /api/v1/predict-simulation/generate
Authorization: Bearer TOKEN
Content-Type: application/json

请求体:
{
  "start_time": "2026-03-20T00:00:00",
  "run_type": "forecast",
  "hours": 24
}

返回: 生成的仿真配置
```

#### 删除仿真记录
```
DELETE /api/v1/predict-simulation/record/{run_uuid}
Authorization: Bearer TOKEN

返回:
{
  "status": "success"
}
```

#### 初始化仿真
```
POST /api/v1/predict-simulation/init
Authorization: Bearer TOKEN
Content-Type: application/json

请求体: 初始化参数

返回: 初始化结果
```

#### 仿真动作
```
POST /api/v1/predict-simulation/{uuid}/action/idle
POST /api/v1/predict-simulation/{uuid}/action/charge-from-renewable
POST /api/v1/predict-simulation/{uuid}/action/charge-from-grid
POST /api/v1/predict-simulation/{uuid}/action/discharge-full-coverage
Authorization: Bearer TOKEN
Content-Type: application/json

参数:
- step_id: 步骤ID (必填)

请求体:
{
  "step_id": 1,
  "max_charge_kw": 5000
}

返回: 动作执行结果
```

#### 执行仿真步骤
```
POST /api/v1/predict-simulation/{uuid}/step
Authorization: Bearer TOKEN
Content-Type: application/json

参数:
- step_id: 步骤ID (必填)

请求体:
{
  "dt_sec": 3600
}

返回: 步骤执行结果
```

#### 仿真WebSocket
```
WebSocket /api/v1/predict-simulation/{uuid}/ws

用于实时接收仿真进度更新
```

#### 自动运行仿真
```
POST /api/v1/predict-simulation/{uuid}/run
Authorization: Bearer TOKEN

返回:
{
  "status": "success",
  "message": "Auto-run started",
  "run_type": "forecast_auto",
  "run_status": "running"
}
```

#### 暂停仿真
```
POST /api/v1/predict-simulation/{uuid}/pause
Authorization: Bearer TOKEN

返回:
{
  "status": "success",
  "message": "Simulation paused",
  "run_type": "forecast",
  "run_status": "paused"
}
```

#### 获取仿真摘要
```
GET /api/v1/predict-simulation/{uuid}/summary
Authorization: Bearer TOKEN

返回: 仿真执行摘要
```

#### 清理仿真资源
```
POST /api/v1/predict-simulation/cleanup
Authorization: Bearer TOKEN
Content-Type: application/json

请求体: 清理参数

返回: 清理结果
```

---

## 常见场景与推荐接口

### 场景1: 本周每日用电量和电费趋势
- 推荐接口: `GET /api/v1/billing/daily/history/list?start_date={本周一}&end_date={今天}`
- 或使用: `GET /api/v1/energy-trends/trend/electricity_cost?start_date={本周一}&end_date={今天}`

### 场景2: 今日电价变化趋势
- 推荐接口: `GET /api/v1/energy-extended/price-load-overlay?hours=24`

### 场景3: 储能系统当前状态
- 推荐接口: `GET /api/v1/energy-extended/storage-status`
- 推荐接口: `GET /api/v1/energy/storage-revenue/realtime`

### 场景4: AI智能调度建议
- 推荐接口: `GET /api/v1/external-services/ai-recommendations/latest`

### 场景5: 负载预测
- 推荐接口: `GET /api/v1/energy/load-forecast/data?hours=24`
- 短期预测: `GET /api/v1/energy/forecast/short?hours=24`

### 场景6: 削峰填谷效果
- 推荐接口: `GET /api/v1/energy/peak-shaving/daily-metrics?date=YYYY-MM-DD`
- 推荐接口: `GET /api/v1/energy/storage-revenue/realtime`

### 场景7: 集群功率监控
- 推荐接口: `GET /api/v1/cluster/overview`
- 推荐接口: `GET /api/v1/compute/cluster/power/realtime`

### 场景8: 绿电占比历史趋势
- 推荐接口: `GET /api/v1/green-energy/ratio/history?start_date={开始}&end_date={结束}`
- 或使用: `GET /api/v1/energy-trends/trend/green_ratio?start_date={开始}&end_date={结束}`

### 场景9: CO2减排统计
- 推荐接口: `GET /api/v1/energy-trends/trend/co2_reduction?start_date={开始}&end_date={结束}`
- 推荐接口: `GET /api/v1/esg/summary`

### 场景10: 储能节省分析
- 推荐接口: `GET /api/v1/energy-trends/trend/savings?start_date={开始}&end_date={结束}`

### 场景11: 策略配置管理
- 查看策略: `GET /api/v1/strategies/configs`
- 应用策略: `POST /api/v1/strategies/configs/{id}/apply`

### 场景12: 调度状态监控
- 调度状态: `GET /api/v1/strategy/status`
- 调度概览: `GET /api/v1/strategy/overview`

---

## 注意事项

1. **时间格式**: ISO 8601 (如 `2026-03-20T15:30:00`)
2. **日期格式**: `YYYY-MM-DD`
3. **电价单位**: 元/kWh
4. **功率单位**: kW
5. **电量单位**: kWh
6. **金额单位**: 元
7. **SOC单位**: 百分比 (0-100)
8. **绿电占比**: 可表示为比例 (0-1) 或百分比 (0-100)
9. **CO2减排**: 单位为吨 (ton) 或千克 (kg)
