---
title: NVLink / NVSwitch
type: concept
date: 2026-04-14
sources:
  - 竞品芯片分析-2026.md
related:
  - entity/nvidia
  - concept/ai芯片竞争格局
---

# NVLink / NVSwitch

## 定义

**NVLink** 是 NVIDIA 开发的高速点对点串行通信协议，用于实现 GPU 之间、GPU 与 CPU 之间的高速、低延迟、高带宽互联。

**NVSwitch** 是 NVIDIA 的 GPU 桥接交换芯片，可提供多 GPU 之间的全互联（all-to-all）通信能力。

## 技术演进

| 版本 | 单向带宽 | 主要应用 |
|------|----------|----------|
| NVLink v1 | 20 GB/s | P100 |
| NVLink v2 | 25 GB/s | V100 |
| NVLink v3 | 25 GB/s | A100 |
| NVLink v4 | 25 GB/s（单链路） | H100 / H200 / B200 |

- **NVSwitch v2**：18 个 Port，每 Port 双向 50GB/s，总带宽 900GB/s。
- **NVSwitch v3**：64 个 Port，总带宽 3.2TB/s。

## 互联形态

1. **两 GPU NVLink Bridge 互联**：通过桥接器连接两张 PCIe GPU。
2. **四 GPU NVLink 全互联**：任意两 GPU 间通过 4 条 NVLink 连接，双向带宽 200GB/s。
3. **八 GPU NVSwitch 全互联**（DGX-A100）：单主板 8 GPU，6 个 NVSwitch，总双向带宽 2.4TB/s。
4. **十六 GPU NVSwitch 全互联**（DGX-2）：跨主板互联，12 个 NVSwitch 2.0，总双向带宽 2.4TB/s。

## 实测性能

- **4 卡 V100**：实测单向带宽约 48.5GB/s，双向约 97GB/s（理论值 50GB/s / 100GB/s）。
- **8 卡 A100（NVSwitch）**：实测单向带宽约 270GB/s，双向约 500GB/s。

## 意义

在大模型分布式训练中，NVLink/NVSwitch 是降低通信瓶颈、提升多卡扩展效率的关键基础设施。
