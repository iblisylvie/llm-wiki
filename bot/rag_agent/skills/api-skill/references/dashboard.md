# 图表数据格式规范

本文档定义智能 Dashboard 的统一 JSON 协议。外部 agent、nanobot、skill、以及前端 debug 模式都必须遵循这套格式，前端只消费这一套协议。

本文档的目标不是描述 agent 的实现过程，而是定义 agent / skill 最终必须产出的结果格式。

---

## 通用说明

### 协议适用范围

本协议统一适用于以下场景：

- 外部 agent 生成 Dashboard JSON
- nanobot / skill 调后端接口后生成图表 JSON
- 前端 debug 模式下手工添加组件
- Dashboard 创建/更新接口的 payload

### 设计原则

1. `DashboardConfig` 是顶层对象
2. `WidgetConfig` 是前端可直接渲染的最小单元
3. `options` 只描述展示方式
4. `data` 只描述图表渲染所需业务数据
5. agent / skill 可以自由决定如何取数和聚合，但最终输出必须是“已解析完成”的 JSON，前端不感知其中间过程

### 数据结构层次
```
DashboardConfig
├── id: string
├── name: string
├── layout: DashboardLayout
└── widgets: WidgetConfig[]

WidgetConfig
├── id: string              // 组件唯一标识
├── type: WidgetType        // 图表类型
├── title: string           // 标题
├── position: { x, y }      // 位置
├── size: { width, height } // 尺寸
├── options: WidgetOptions  // 图表配置（样式、颜色等）
└── data: WidgetData        // 图表数据（本规范重点）
```

### 顶层结构

```json
{
  "id": "energy-overview-dashboard",
  "name": "能源总览仪表盘",
  "layout": {
    "type": "grid",
    "columns": 12,
    "rowHeight": 80,
    "gap": 16
  },
  "generatedBy": "skill",
  "widgets": [
    {
      "id": "metric-pue",
      "type": "metric",
      "title": "PUE",
      "position": { "x": 0, "y": 0 },
      "size": { "width": 3, "height": 1 },
      "options": { "decimals": 2, "trend": true },
      "data": {
        "value": 1.35,
        "trend": {
          "direction": "down",
          "value": -0.05,
          "percentage": -3.57,
          "label": "较昨日"
        }
      }
    }
  ]
}
```

### 通用配置字段 (options)
所有图表共享的配置项：
```json
{
  "colors": ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"],
  "showLegend": true,
  "showTooltip": true,
  "animation": true,
  "height": 300
}
```

### 通用校验规则

- `id` 在同一个 `DashboardConfig` 内必须唯一
- `layout.type` 一期固定为 `grid`
- `position.x + size.width` 不得超过总列数
- `size.width`、`size.height` 必须大于 0
- 对于 `labels + datasets` 结构，所有 `datasets[].data.length` 必须与 `labels.length` 一致
- 对于 `radar`，`datasets[].values.length` 必须与 `indicators.length` 一致
- 对于 `scatter`，每个点必须至少包含 `x` 和 `y`
- 前端手工 debug 数据与 AI 生成数据，必须完全遵守相同校验规则

---

## 1. 指标卡 (metric)

### 数据格式
```json
{
  "type": "metric",
  "title": "PUE",
  "options": {
    "unit": "",
    "decimals": 2,
    "trend": true,
    "comparison": true,
    "sparkline": true,
    "colorTheme": "auto"
  },
  "data": {
    "value": 1.35,
    "unit": "",
    "formatted": "1.35",
    "trend": {
      "direction": "down",
      "value": -0.05,
      "percentage": -3.57,
      "label": "较昨日"
    },
    "comparison": {
      "label": "行业平均",
      "value": 1.5,
      "status": "good"
    },
    "sparkline": {
      "data": [1.42, 1.40, 1.38, 1.36, 1.35, 1.34, 1.35],
      "color": "#10B981"
    },
    "thresholds": {
      "warning": 1.4,
      "critical": 1.6
    }
  }
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| value | number | ✅ | 主指标值 |
| unit | string | ❌ | 单位 |
| formatted | string | ❌ | 格式化后的显示文本 |
| trend.direction | string | ❌ | 趋势方向: up/down/flat |
| trend.value | number | ❌ | 变化值 |
| trend.percentage | number | ❌ | 变化百分比 |
| trend.label | string | ❌ | 对比基准描述 |
| comparison | object | ❌ | 对比参照 |
| sparkline.data | number[] | ❌ | 迷你趋势图数据 |
| thresholds | object | ❌ | 阈值配置 |

---

## 2. 柱状图 (bar)

### 数据格式
```json
{
  "type": "bar",
  "title": "各区域能耗分布",
  "options": {
    "xAxis": {
      "label": "区域",
      "rotate": 0
    },
    "yAxis": {
      "label": "能耗 (kWh)",
      "min": 0
    },
    "bar": {
      "width": 0.6,
      "radius": [4, 4, 0, 0]
    },
    "stacked": false,
    "showGrid": true,
    "showValues": false
  },
  "data": {
    "labels": ["A区", "B区", "C区", "D区", "E区"],
    "datasets": [
      {
        "name": "照明",
        "data": [1200, 1900, 800, 1500, 2000],
        "color": "#3B82F6"
      },
      {
        "name": "空调",
        "data": [2500, 3200, 1800, 2800, 3500],
        "color": "#10B981"
      },
      {
        "name": "设备",
        "data": [3800, 4200, 3500, 4000, 4500],
        "color": "#F59E0B"
      }
    ]
  }
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| labels | string[] | ✅ | X轴标签 |
| datasets | array | ✅ | 数据系列数组 |
| datasets[].name | string | ✅ | 系列名称（图例） |
| datasets[].data | number[] | ✅ | 数值数组，与labels一一对应 |
| datasets[].color | string | ❌ | 系列颜色 |
| datasets[].stack | string | ❌ | 堆叠分组标识 |

---

## 3. 折线图 (line)

### 数据格式
```json
{
  "type": "line",
  "title": "功率曲线",
  "options": {
    "xAxis": {
      "label": "时间",
      "format": "HH:mm",
      "tickInterval": "auto"
    },
    "yAxis": {
      "label": "功率 (MW)",
      "min": 0
    },
    "line": {
      "width": 2,
      "smooth": true,
      "dot": true,
      "dotSize": 4
    },
    "showGrid": true,
    "fillArea": false
  },
  "data": {
    "labels": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "24:00"],
    "datasets": [
      {
        "name": "总负荷",
        "data": [45, 42, 55, 78, 82, 68, 52],
        "color": "#3B82F6"
      },
      {
        "name": "光伏出力",
        "data": [0, 0, 15, 45, 52, 28, 0],
        "color": "#F59E0B"
      },
      {
        "name": "风电出力",
        "data": [18, 22, 15, 12, 20, 25, 22],
        "color": "#10B981"
      }
    ]
  }
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| labels | string[] | ✅ | X轴标签（时间点） |
| datasets | array | ✅ | 数据系列数组 |
| datasets[].name | string | ✅ | 系列名称 |
| datasets[].data | number[] | ✅ | 数值数组 |
| datasets[].color | string | ❌ | 线条颜色 |
| datasets[].dashed | boolean | ❌ | 是否虚线 |

---

## 4. 条形图 (bar-h)

### 数据格式
```json
{
  "type": "bar-h",
  "title": "设备能耗排名",
  "options": {
    "xAxis": {
      "label": "能耗 (kWh)"
    },
    "yAxis": {
      "label": ""
    },
    "bar": {
      "height": 24,
      "radius": [0, 4, 4, 0]
    },
    "showValues": true,
    "valuePosition": "right"
  },
  "data": {
    "labels": ["GPU集群A", "GPU集群B", "制冷系统", "UPS电源", "照明系统"],
    "datasets": [
      {
        "name": "能耗",
        "data": [12500, 11200, 8500, 6200, 3500],
        "colors": ["#EF4444", "#F59E0B", "#F59E0B", "#3B82F6", "#10B981"]
      }
    ]
  }
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| labels | string[] | ✅ | Y轴标签（从上到下） |
| datasets[0].data | number[] | ✅ | 数值数组 |
| datasets[0].colors | string[] | ❌ | 每个条形的独立颜色 |

---

## 5. 面积图 (area)

### 数据格式
```json
{
  "type": "area",
  "title": "储能SOC变化趋势",
  "options": {
    "xAxis": {
      "label": "时间",
      "format": "HH:mm"
    },
    "yAxis": {
      "label": "SOC (%)",
      "min": 0,
      "max": 100
    },
    "area": {
      "opacity": 0.3,
      "gradient": true
    },
    "line": {
      "width": 2,
      "smooth": true
    },
    "stacked": false
  },
  "data": {
    "labels": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
    "datasets": [
      {
        "name": "SOC",
        "data": [85, 45, 30, 75, 90, 65],
        "color": "#10B981",
        "fillColor": "#10B981"
      }
    ]
  }
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| labels | string[] | ✅ | X轴标签 |
| datasets[].data | number[] | ✅ | 数值数组 |
| datasets[].color | string | ✅ | 边界线颜色 |
| datasets[].fillColor | string | ❌ | 填充颜色（默认同color） |
| datasets[].stack | string | ❌ | 堆叠分组标识 |

---

## 6. 饼图 (pie)

### 数据格式
```json
{
  "type": "pie",
  "title": "能源结构占比",
  "options": {
    "showLegend": true,
    "legendPosition": "right",
    "showLabels": true,
    "labelFormat": "percentage",
    "innerRadius": 0
  },
  "data": {
    "segments": [
      {
        "name": "光伏",
        "value": 4500,
        "color": "#F59E0B"
      },
      {
        "name": "风电",
        "value": 2800,
        "color": "#10B981"
      },
      {
        "name": "储能放电",
        "value": 1200,
        "color": "#8B5CF6"
      },
      {
        "name": "电网",
        "value": 3500,
        "color": "#6B7280"
      }
    ],
    "total": 12000
  }
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| segments | array | ✅ | 扇区数组 |
| segments[].name | string | ✅ | 扇区名称 |
| segments[].value | number | ✅ | 数值 |
| segments[].color | string | ❌ | 扇区颜色（不填则使用默认色板） |
| total | number | ❌ | 总计值（用于百分比计算） |

---

## 7. 环状图 (donut)

### 数据格式
```json
{
  "type": "donut",
  "title": "负荷类型分布",
  "options": {
    "innerRadius": 0.6,
    "showLegend": true,
    "legendPosition": "bottom",
    "centerText": {
      "main": "总负荷",
      "sub": "85 MW"
    }
  },
  "data": {
    "segments": [
      {
        "name": "算力负载",
        "value": 52,
        "color": "#3B82F6"
      },
      {
        "name": "制冷系统",
        "value": 18,
        "color": "#10B981"
      },
      {
        "name": "照明及其他",
        "value": 8,
        "color": "#F59E0B"
      },
      {
        "name": "网络设备",
        "value": 7,
        "color": "#8B5CF6"
      }
    ],
    "total": 85
  }
}
```

### 字段说明
与饼图相同，额外增加：
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| options.innerRadius | number | ❌ | 内圈半径比例（0-1），默认0.6 |
| options.centerText | object | ❌ | 中心文字配置 |

---

## 8. 组合图 (compose)

### 数据格式
```json
{
  "type": "compose",
  "title": "能源供需对比",
  "options": {
    "xAxis": {
      "label": "时间"
    },
    "yAxis": [
      {
        "label": "功率 (MW)",
        "position": "left"
      },
      {
        "label": "电价 (元/kWh)",
        "position": "right"
      }
    ],
    "showGrid": true
  },
  "data": {
    "labels": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
    "datasets": [
      {
        "name": "总负荷",
        "type": "area",
        "data": [45, 42, 55, 78, 82, 68],
        "color": "#3B82F6",
        "yAxisIndex": 0
      },
      {
        "name": "绿电出力",
        "type": "area",
        "data": [18, 22, 30, 57, 72, 53],
        "color": "#10B981",
        "yAxisIndex": 0
      },
      {
        "name": "电价",
        "type": "line",
        "data": [0.35, 0.35, 0.85, 1.20, 1.20, 0.65],
        "color": "#EF4444",
        "yAxisIndex": 1,
        "dashed": true
      }
    ]
  }
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| datasets[].type | string | ✅ | 图表类型: bar/line/area |
| datasets[].yAxisIndex | number | ❌ | Y轴索引（0=左, 1=右） |
| datasets[].dashed | boolean | ❌ | 是否虚线（line类型） |

---

## 9. 雷达图 (radar)

### 数据格式
```json
{
  "type": "radar",
  "title": "数据中心综合评估",
  "options": {
    "shape": "polygon",
    "splitNumber": 5,
    "showAxisLine": true,
    "showSplitArea": true,
    "splitAreaOpacity": 0.1
  },
  "data": {
    "indicators": [
      {
        "name": "能效",
        "max": 100
      },
      {
        "name": "可靠性",
        "max": 100
      },
      {
        "name": "绿电占比",
        "max": 100
      },
      {
        "name": "成本控制",
        "max": 100
      },
      {
        "name": "设备健康",
        "max": 100
      },
      {
        "name": "负载均衡",
        "max": 100
      }
    ],
    "datasets": [
      {
        "name": "当前",
        "values": [85, 92, 78, 70, 88, 82],
        "color": "#3B82F6"
      },
      {
        "name": "行业平均",
        "values": [75, 80, 60, 65, 75, 70],
        "color": "#9CA3AF"
      }
    ]
  }
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| indicators | array | ✅ | 维度指标数组 |
| indicators[].name | string | ✅ | 维度名称 |
| indicators[].max | number | ✅ | 该维度最大值 |
| datasets[].values | number[] | ✅ | 各维度数值，与indicators一一对应 |
| datasets[].color | string | ❌ | 系列颜色 |

---

## 10. 散点图 (scatter)

### 数据格式
```json
{
  "type": "scatter",
  "title": "功率与温度相关性",
  "options": {
    "xAxis": {
      "label": "环境温度 (°C)",
      "min": 15,
      "max": 40
    },
    "yAxis": {
      "label": "功率 (MW)",
      "min": 0
    },
    "symbolSize": 10,
    "showRegressionLine": true
  },
  "data": {
    "datasets": [
      {
        "name": "A区",
        "points": [
          {"x": 22, "y": 45, "size": 10},
          {"x": 25, "y": 48, "size": 12},
          {"x": 28, "y": 52, "size": 15},
          {"x": 30, "y": 55, "size": 14},
          {"x": 32, "y": 58, "size": 16}
        ],
        "color": "#3B82F6"
      },
      {
        "name": "B区",
        "points": [
          {"x": 20, "y": 38, "size": 8},
          {"x": 24, "y": 42, "size": 10},
          {"x": 27, "y": 46, "size": 12},
          {"x": 31, "y": 51, "size": 14}
        ],
        "color": "#10B981"
      }
    ]
  }
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| datasets[].points | array | ✅ | 散点数组 |
| points[].x | number | ✅ | X坐标值 |
| points[].y | number | ✅ | Y坐标值 |
| points[].size | number | ❌ | 散点大小（气泡图用） |
| points[].label | string | ❌ | 散点标签 |

---

## 11. 漏斗图 (funnel)

### 数据格式
```json
{
  "type": "funnel",
  "title": "能源转化效率",
  "options": {
    "sort": "descending",
    "gap": 2,
    "showLabels": true,
    "labelPosition": "inside",
    "funnelAlign": "center"
  },
  "data": {
    "stages": [
      {
        "name": "绿电输入",
        "value": 10000,
        "percentage": 100
      },
      {
        "name": "变压器转换",
        "value": 9500,
        "percentage": 95
      },
      {
        "name": "UPS稳压",
        "value": 9120,
        "percentage": 96
      },
      {
        "name": "PDU分配",
        "value": 8664,
        "percentage": 95
      },
      {
        "name": "IT设备使用",
        "value": 7884,
        "percentage": 91
      }
    ]
  }
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| stages | array | ✅ | 阶段数组（从上到下） |
| stages[].name | string | ✅ | 阶段名称 |
| stages[].value | number | ✅ | 数值 |
| stages[].percentage | number | ❌ | 百分比（相对上一阶段） |
| stages[].color | string | ❌ | 阶段颜色 |

---

## 12. 词云 (wordcloud)

### 数据格式
```json
{
  "type": "wordcloud",
  "title": "告警关键词分析",
  "options": {
    "minFontSize": 12,
    "maxFontSize": 48,
    "rotation": [-45, 0, 45],
    "shape": "circle",
    "padding": 4
  },
  "data": {
    "words": [
      {
        "text": "温度过高",
        "weight": 85,
        "color": "#EF4444"
      },
      {
        "text": "SOC偏低",
        "weight": 72,
        "color": "#F59E0B"
      },
      {
        "text": "网络延迟",
        "weight": 58,
        "color": "#3B82F6"
      },
      {
        "text": "GPU利用率",
        "weight": 45,
        "color": "#10B981"
      },
      {
        "text": "电压波动",
        "weight": 38,
        "color": "#8B5CF6"
      },
      {
        "text": "储能健康",
        "weight": 32,
        "color": "#6B7280"
      },
      {
        "text": "负载均衡",
        "weight": 28,
        "color": "#6B7280"
      },
      {
        "text": "制冷效率",
        "weight": 24,
        "color": "#6B7280"
      }
    ]
  }
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| words | array | ✅ | 词语数组 |
| words[].text | string | ✅ | 词语文本 |
| words[].weight | number | ✅ | 权重（决定字体大小） |
| words[].color | string | ❌ | 词语颜色（不填则自动分配） |
| words[].category | string | ❌ | 分类（可用于颜色分组） |

---

## 附录A: 类型定义 (TypeScript)

```typescript
// ===== 通用类型 =====
type TrendDirection = 'up' | 'down' | 'flat';

interface TrendInfo {
  direction: TrendDirection;
  value: number;
  percentage: number;
  label: string;
}

interface ChartDataset {
  name: string;
  data: number[];
  color?: string;
}

// ===== 各图表数据类型 =====

// 1. 指标卡
interface MetricData {
  value: number;
  unit?: string;
  formatted?: string;
  trend?: TrendInfo;
  comparison?: {
    label: string;
    value: number;
    status: 'good' | 'warning' | 'bad';
  };
  sparkline?: {
    data: number[];
    color?: string;
  };
  thresholds?: {
    warning?: number;
    critical?: number;
  };
}

// 2-5. 基础图表
interface BasicChartData {
  labels: string[];
  datasets: ChartDataset[];
}

// 6-7. 饼图/环状图
interface PieSegment {
  name: string;
  value: number;
  color?: string;
}

interface PieChartData {
  segments: PieSegment[];
  total?: number;
}

// 8. 组合图
interface ComposeDataset extends ChartDataset {
  type: 'bar' | 'line' | 'area';
  yAxisIndex?: number;
  dashed?: boolean;
}

interface ComposeChartData {
  labels: string[];
  datasets: ComposeDataset[];
}

// 9. 雷达图
interface RadarIndicator {
  name: string;
  max: number;
}

interface RadarDataset {
  name: string;
  values: number[];
  color?: string;
}

interface RadarChartData {
  indicators: RadarIndicator[];
  datasets: RadarDataset[];
}

// 10. 散点图
interface ScatterPoint {
  x: number;
  y: number;
  size?: number;
  label?: string;
}

interface ScatterDataset {
  name: string;
  points: ScatterPoint[];
  color?: string;
}

interface ScatterChartData {
  datasets: ScatterDataset[];
}

// 11. 漏斗图
interface FunnelStage {
  name: string;
  value: number;
  percentage?: number;
  color?: string;
}

interface FunnelChartData {
  stages: FunnelStage[];
}

// 12. 词云
interface WordCloudItem {
  text: string;
  weight: number;
  color?: string;
  category?: string;
}

interface WordCloudData {
  words: WordCloudItem[];
}
```

---

## 附录B: 完整Widget配置示例

```json
{
  "id": "chart-power-curve",
  "type": "line",
  "title": "24小时功率曲线",
  "position": { "x": 0, "y": 1 },
  "size": { "width": 8, "height": 3 },
  "options": {
    "xAxis": {
      "label": "时间",
      "format": "HH:mm"
    },
    "yAxis": {
      "label": "功率 (MW)",
      "min": 0
    },
    "line": {
      "width": 2,
      "smooth": true,
      "dot": true
    },
    "showLegend": true,
    "showGrid": true,
    "colors": ["#3B82F6", "#10B981", "#F59E0B"]
  },
  "data": {
    "labels": ["00:00", "02:00", "04:00", "06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"],
    "datasets": [
      {
        "name": "总负荷",
        "data": [45, 43, 42, 44, 55, 68, 78, 82, 80, 75, 68, 52]
      },
      {
        "name": "光伏出力",
        "data": [0, 0, 0, 5, 25, 42, 48, 52, 45, 28, 8, 0]
      },
      {
        "name": "风电出力",
        "data": [18, 20, 22, 18, 15, 12, 10, 14, 18, 22, 24, 20]
      }
    ]
  }
}
```

---

## 附录C: 智能体生成指南

智能体在生成图表配置时，应遵循以下规则：

### 1. 图表类型选择
| 分析目的 | 推荐图表 |
|----------|----------|
| 展示单一KPI | metric |
| 分类对比 | bar, bar-h |
| 时间趋势 | line, area |
| 占比分析 | pie, donut |
| 多维度评估 | radar |
| 相关性分析 | scatter |
| 转化/效率分析 | funnel |
| 文本分析 | wordcloud |
| 多指标混合 | compose |

### 2. 颜色使用规范
```
主色系：
- 蓝色 #3B82F6：主数据、算力相关
- 绿色 #10B981：能源、环保、正向指标
- 黄色 #F59E0B：光伏、警告、中性指标
- 红色 #EF4444：异常、负向指标
- 紫色 #8B5CF6：储能、特殊指标
- 灰色 #6B7280：次要数据、参照数据
```

### 3. 数据格式化
- 大数值：使用 `toLocaleString()` 格式化
- 百分比：保留1位小数，添加 `%` 后缀
- 货币：保留2位小数，添加 `¥` 前缀
- 时间：使用 `HH:mm` 格式
