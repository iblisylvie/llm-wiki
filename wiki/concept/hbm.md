---
title: HBM（高带宽内存）
type: concept
date: 2026-04-14
sources:
  - 竞品芯片分析-2026.md
related:
  - entity/nvidia
  - concept/ai芯片竞争格局
  - concept/推理优化
---

# HBM（High Bandwidth Memory，高带宽内存）

## 定义

HBM 是一种 3D 堆叠内存技术，通过硅通孔（TSV）将多层 DRAM 芯片垂直堆叠，并与 GPU/CPU 封装在同一基板上，从而实现极高的内存带宽和较低的功耗。

## HBM vs GDDR

| 特性 | HBM | GDDR |
|------|-----|------|
| 带宽 | 极高（1-4 TB/s 级别） | 中等（数百 GB/s 级别） |
| 容量 | 较大（24-192GB） | 较小（8-48GB） |
| 功耗 | 较低（单位带宽功耗低） | 较高 |
| 成本 | 高 | 较低 |
| 典型应用 | 训练卡（A100、H100、MI300X） | 推理卡、游戏 GPU（T4、RTX 4090） |

## 典型产品的 HBM 配置

| 产品 | HBM 类型 | 容量 | 带宽 |
|------|----------|------|------|
| A100 | HBM2e | 80GB | 1.935 TB/s |
| H100 | HBM3 | 80GB | 3.35 TB/s |
| H200 | HBM3 | 141GB | 4.8 TB/s |
| MI300X | HBM3 | 192GB | 5.2 TB/s |
| 昇腾 910C | HBM2e | 128GB | 3.2 TB/s |
| 昆仑芯 P800 | — | 96GB | 2.76 TB/s |

## 大模型场景中的关键性

随着 LLM 参数规模增大，**推理阶段往往从 Compute-bound 转向 Memory-bound**（IO-bound）。显存容量决定了能加载多大的模型，显存带宽决定了 token 生成速度。HBM 因此成为高端 AI 芯片的必备配置。

## 产业趋势

- **HBM3e / HBM4**：下一代标准，带宽和容量继续提升。
- **国产替代**：中国厂商在 HBM 封装和 DRAM 方面加速布局自主可控能力。
