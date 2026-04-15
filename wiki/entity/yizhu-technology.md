---
title: 亿铸科技
type: entity
date: 2026-04-15
sources:
  - yizhu-expo-qa-2026-04-15.md
related:
  - concept/processing-in-memory
  - concept/fp8
  - concept/ai-chip-landscape
---

# 亿铸科技（Yizhu Technology）

## 概述

亿铸科技是一家专注于**存算一体（PIM, Processing-in-Memory）AI 芯片**的国内厂商，主打云端大模型推理场景。

## 代表产品

- **G100**：旗舰存算一体 AI 芯片
  - 存储介质：**DRAM**（针对云端大存储空间需求选择，非 ReRAM）
  - 目标市场：云端大模型推理、大模型一体机（训推一体）
  - 数据精度：原生支持 **FP8**
  - 推理性能：硬件模拟环境实测最高吞吐约 **7000 Token/秒**
  - 板间互联：PCIe 5.0（32GB/s）或 RDMA 1×200Gbps
  - 计划商用时间：**2026 年 Q1**
  - 生产制程：国内完成生产封装，供应链自主可控

## 技术特点

1. **存算一体架构**
   - 计算单元与存储单元深度融合，本地直接处理数据
   - 宣称可消除 90% 以上的数据搬运时间和能耗

2. **CUDA 兼容策略**
   - 硬件 ISA 兼容 NVIDIA PTX（虚拟指令集）
   - 软件栈基于 **PyTorch + Triton**
   - 后端编译器可自动加速 LLVM IR，兼容 CUDA 与 CUDA-Free 生态

3. **自研 AI 编译器**
   - 集成 AutoSearch 搜索优化器
   - 自动算子生成 + 自动调优（含底层可执行代码调优）
   - 降低模型适配和迁移的人力成本

## 市场定位

- 对标国际主流大模型推理 AI 芯片（NVIDIA H100/H200 级别）
- 重点推进大模型一体机市场，目标支持**满血版 DeepSeek FP8** 全精度推理部署
