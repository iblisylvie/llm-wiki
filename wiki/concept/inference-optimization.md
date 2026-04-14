---
title: 推理优化
type: concept
date: 2026-04-14
sources:
  - 讯飞转写_2026年03月28日_直播笔记_浦江智涌_AI无界_Physical_AI_前沿探索与产业创新研讨会暨第二十八届系友论坛顺利举办_Part2.txt
related:
  - source/xunfei-2026-03-28-physical-ai-symposium-part2.md
  - entity/oriental-computing.md
  - concept/advanced-packaging.md
---

# 推理优化

## 定义

推理优化（Inference Optimization）是指针对大语言模型和生成式 AI 在推理（Inference）阶段进行的性能、成本和延迟优化。与训练阶段追求"算力峰值"不同，推理阶段的核心瓶颈往往是内存带宽和访存效率。

## 核心优化方向

### 1. Prefill/Decode 分离（P/D Separation）

大模型推理分为两个阶段：
- **Prefill 阶段**：处理输入提示（Prompt），计算量大、可并行
- **Decode 阶段**：逐 Token 生成输出，受限于内存带宽

分离优化的核心思路：针对两个阶段的计算特征差异，采用不同的硬件配置和调度策略。

### 2. 缓解 Decode 带宽瓶颈

生成阶段的主要瓶颈不是算力，而是**内存带宽**（从 HBM/DRAM 读取模型参数和 KV Cache）。优化手段包括：
- 模型量化（INT8/INT4）
- KV Cache 压缩与优化
- 投机采样（Speculative Decoding）
- 批处理（Batching）和连续批处理（Continuous Batching）

### 3. SRAM 优化

- 通过稀疏激活、专家混合（MoE）等手段，减少每次推理需要加载的参数量
- 提升片上 SRAM 的利用率，减少对外部内存的访问

## 产业判断

> "训练看算力，推理看带宽；未来 AI 芯片的竞争将从 Training 转向 Inference。"

在 2026-03-28 的研讨会上，嘉宾普遍认为随着大模型部署规模扩大，推理成本和效率将成为产业链竞争的核心焦点。

## 来源

- [浦江智涌 AI无界 Physical AI 研讨会（下午场）](../source/xunfei-2026-03-28-physical-ai-symposium-part2.md)
