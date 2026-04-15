---
title: 登临科技
type: entity
date: 2026-04-14
sources:
  - competitor-chip-analysis-2026.md
related:
  - concept/ai-chip-landscape
---

# 登临科技（Denglin）

## 概述

登临科技是一家 AI 芯片初创企业，产品主打边缘和数据中心推理场景，采用"GPU+"架构。

## 代表产品

- **Goldwasser L256**：边缘/数据中心推理卡，INT8 256 TOPS / FP16 64 TFLOPS，32-64GB 显存，PCIe 3.0 ×16，功耗 45W，半高半长。
- **Goldwasser XL**：升级版本，INT8 512 TOPS / FP16 128 TFLOPS，PCIe 3.0 ×16，功耗 120W，全高全长。
- **Goldwasser II GS40**：数据中心推理卡，INT8 512 TOPS / FP16 256 TFLOPS / TF32 128 TFLOPS，32/64/128GB 显存，PCIe 5.0 ×16，功耗 60W。

## 劣势与挑战

- **软件成熟度不足**：客户反馈存在多项严重问题：
  - SDK 版本间模型文件不兼容，尚无解决方案。
  - 模型转换报错信息不足，难以定位问题。
  - 序列化后的模型文件体积膨胀严重（原始模型的 5-20 倍，小模型甚至 200 倍）。
  - 硬件缩放单元局限性大，CUDA 核心预处理性能与 T4 存在差距。
  - 多路视频解析能力与同价位国产方案相比仍有差距。
