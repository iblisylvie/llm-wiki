---
title: Tensor Core
type: concept
date: 2026-04-14
sources:
  - 竞品芯片分析-2026.md
related:
  - entity/nvidia
  - concept/ai芯片竞争格局
---

# Tensor Core

## 定义

Tensor Core 是 NVIDIA 从 **Volta 架构**（V100）开始引入的特殊计算单元，专门用于加速矩阵乘法和累加运算（D = A × B + C），这是深度学习训练和推理中最核心的操作。

## 与 CUDA Core 的区别

- **CUDA Core**：一个时钟周期只能完成 1 次浮点乘加（FFMA）。
- **Tensor Core**：一个时钟周期可以完成**一组**矩阵乘加运算，例如 4×4×4 或 8×4×8 的矩阵乘法。

## 算力对比（理论值）

| 架构 | 产品 | 单次 FFMA 数量 | Tensor Core FP16 算力 |
|------|------|----------------|----------------------|
| Volta | V100 | 64 | 125 TFLOPS |
| Ampere | A100 | 256 | 311 TFLOPS |
| Hopper | H100 | 更大规模 | 989-1979 TFLOPS |

相比之下，A100 的 CUDA Core FP32 算力仅约 19.5 TFLOPS，Tensor Core 的矩阵运算效率远超 CUDA Core。

## 支持的数据类型演进

- **V100**：仅 FP16
- **A100**：FP16、BF16、TF32、INT8
- **H100**：FP8（E5M2、E4M3）、FP16、BF16、TF32、INT8
- **B200/RTX 50**：继续扩展 FP8/FP4 支持

## 重要性

Tensor Core 是 NVIDIA 在 AI 训练/推理领域保持算力优势的核心技术，也是国产 GPU 追赶的关键方向之一。
