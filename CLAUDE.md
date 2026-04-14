# LLM Wiki Schema

本文档定义了这个 wiki 的结构、约定和维护流程。每次与 LLM 交互时，都应遵循这里的规则。

## 目录结构

```
llm_wiki/
├── CLAUDE.md           # 本文件：schema 和约定
├── llm-wiki.md         # 原始理念文档（只读）
├── raw/                # 原始资料（只读）
│   ├── assets/         # 图片、附件等
│   └── ...             # 文章、论文、笔记等
└── wiki/               # LLM 维护的 wiki 页面
    ├── index.md        # 内容索引
    ├── log.md          # 操作日志
    └── ...             # 实体页、概念页、总结页等
```

## 页面类型

- **source/**: 对每篇原始资料的总结页，文件名与 raw/ 中的文件对应。
- **entity/**: 人物、组织、项目、产品等实体页面。
- **concept/**: 概念、理论、方法、术语页面。
- **synthesis/**: 综合分析、比较、专题研究页面。
- **overview.md**: 全局概览和当前主要结论。

## 文件命名约定

- 使用小写英文，单词间用连字符 `-` 连接。
- 例如：`entity/elon-musk.md`, `concept/rag-system.md`

## 页面格式

每个 wiki 页面建议包含 YAML frontmatter：

```yaml
---
title: 页面标题
type: entity | concept | source | synthesis
date: YYYY-MM-DD
sources: []        # 相关的 raw 文件名
related: []        # 相关的 wiki 页面链接
---
```

## 操作流程

### Ingest（摄入资料）

1. 读取 `raw/` 中的新文件。
2. 在 `wiki/source/` 下创建对应的总结页。
3. 提取关键实体和概念，创建或更新 `wiki/entity/` 和 `wiki/concept/` 页面。
4. 更新 `wiki/overview.md` 和 `wiki/index.md`。
5. 在 `wiki/log.md` 中追加一条记录：`## [YYYY-MM-DD] ingest | 资料标题`

### Query（回答问题）

1. 先读取 `wiki/index.md` 找到相关页面。
2. 读取相关页面，综合回答。
3. 如果答案有价值，可作为新页面存入 `wiki/synthesis/`，并更新索引和日志。

### Lint（健康检查）

1. 定期检查页面间的矛盾和过时信息。
2. 查找孤立页面（无入链）。
3. 查找提及但未建页的重要概念。
4. 检查并修复损坏的内部链接。
5. 在 `wiki/log.md` 中记录 lint 结果。

## 当前状态

- 第一批资料已摄入（3 份会议记录）。
- Wiki 页面数：20（3 source + 7 entity + 7 concept + index + log + overview）。
