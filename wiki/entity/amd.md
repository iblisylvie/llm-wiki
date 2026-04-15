---
title: AMD
type: entity
date: 2026-04-14
sources:
  - competitor-chip-analysis-2026.md
related:
  - concept/ai-chip-landscape
  - entity/nvidia
---

# AMD

## 概述

AMD 是全球第二大 GPU 和 CPU 厂商，近年来通过 Instinct 系列加速卡和 MI300X 等产品积极进入 AI 数据中心市场，成为 NVIDIA 的主要竞争对手之一。

## 代表产品

- **Alveo V70**：云推理卡，INT8 404 TOPS / BF16 202 TOPS，采用 5nm/6nm + 3D/2.5D 封装，功耗 75W，PCIe Gen 4/5 ×8，参考价约 2 万元。
- **Instinct MI300X**：旗舰训推一体加速卡，FP8 2.61 PFLOPS / FP16 1.3 PFLOPS / TF32 653.7 TFLOPS / FP32 163.4 TFLOPS / FP64 81.7 TFLOPS，192GB HBM3（5.2TB/s），Infinity Fabric 带宽 896GB/s，PCIe 5.0 ×16，峰值功耗 750W。

## 特点

- **超大显存**：MI300X 配备 192GB HBM3，显存容量超过 NVIDIA H200（141GB）。
- **统一内存架构**：通过 Infinity Fabric 实现 CPU 和 GPU 之间的高速互联。
- **性价比路线**：在部分场景中作为 NVIDIA 的高性价比替代方案。
