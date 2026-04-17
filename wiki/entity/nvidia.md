---
title: NVIDIA
type: entity
date: 2026-04-14
sources:
  - 竞品芯片分析-2026.md
related:
  - concept/tensor-core
  - concept/hbm
  - concept/nvlink
---

# NVIDIA（英伟达）

## 概述

NVIDIA 是全球 AI 芯片市场的绝对领导者，其数据中心 GPU（A100、H100、H200、B200 等）占据大模型训练和推理的主流地位。2024 年，NVIDIA 在中国 AI 加速卡市场的出货量占比仍超过 60%（IDC 数据）。

## 代表产品

### 训练/数据中心卡
- **A100**：Ampere 架构，80GB HBM2e，FP16 312-624 TFLOPS，曾是训练卡标杆。
- **H100/H200**：Hopper 架构，H200 显存升级至 141GB HBM3，带宽 4.8TB/s，专为大模型推理优化。
- **B200/GB200**：Blackwell 架构的新一代产品，通过 NVLink/NVSwitch 实现超大规模集群互联。

### 中国特供版
- **H20**：H100 的阉割版，保留 96-141GB HBM3 和 900GB/s NVLink，但 Tensor Core FP16 算力从 1979 TFLOPS 降至 148 TFLOPS。
- **L20**：L40 阉割版，显存 48GB GDDR6。
- **A800/H800**：此前为中国市场定制的互联带宽降级版，已被禁售。

### 推理/游戏 GPU
- **T4 / L4**：低功耗推理卡，性价比高。
- **RTX 4090 / RTX 5090**：消费级旗舰 GPU，常用于中小规模模型推理和 AI 开发，RTX 5090 配备 32GB GDDR7。

## 核心技术

- **Tensor Core**：从 Volta 架构引入的矩阵计算单元，单周期可完成小型矩阵乘加，算力远超 CUDA Core。
- **NVLink / NVSwitch**：GPU 高速点对点互联，NVSwitch v3 总带宽达 3.2TB/s。
- **GPUDirect**：支持 GPU 与网卡、存储、远程 GPU 的零拷贝直接访问。

## 市场地位

- 技术领先：在算力、显存带宽、软件生态（CUDA）三方面保持显著优势。
- 地缘政治风险：美国出口管制导致高端芯片（A100、H100、A800、H800）对中国禁售，NVIDIA 通过推出性能大幅阉割的特供版维持市场份额。
