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

- **优先使用中文命名文件和目录**，保持语义直观、易于检索。
- 对于**约定俗成的英文专有名词**（如 `NVIDIA`、`AMD`、`token`、`FP8`、`HBM`、`NVLink`、`Tensor Core`、`Physical AI` 等），可保留英文原名，无需强行翻译。
- 文件名中避免无意义的英文缩写，必要时用连字符 `-` 分隔。
- 例如：`entity/英伟达.md`, `concept/存算一体.md`, `source/讯飞-2026-03-28-physical-ai研讨会-part1.md`

## 原始目录结构约定

`raw/` 采用编号分类体系：`00-导航中心`、`01-产品资料`、`02-市场情报`、`03-客户与场景`、`04-解决方案`、`05-竞品分析`、`06-销售支持`、`08-项目管理`、`09-知识库`。常见归类：
- 会议记录/研讨会 → `02-市场情报/行业动态/`
- 竞品参数/对比表 → `05-竞品分析/对比分析/`

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

`sources` 字段应记录从 `raw/` 开始的完整相对路径（如 `02-市场情报/行业动态/会议记录/xxx.txt`），而非仅文件名。

## 操作流程

### Ingest（摄入资料）

1. 读取 `raw/` 中的新文件。
2. 在 `wiki/source/` 下创建对应的总结页，并在页面底部添加"原始资料"链接区块：
   - 使用相对路径 `../../raw/...` 链接回原始文件
   - 示例：`- [原始文件名.txt](../../raw/子目录/原始文件名.txt)`
   - wiki 内部页面链接使用 `../entity/xxx.md` 或 `../concept/xxx.md` 格式
3. 提取关键实体和概念，创建或更新 `wiki/entity/` 和 `wiki/concept/` 页面。
4. 更新 `wiki/overview.md` 和 `wiki/index.md`。
5. 在 `wiki/log.md` 中追加一条记录：`## [YYYY-MM-DD] ingest | 资料标题`

#### 工具：批量迁移 raw 目录

移动 `raw/` 子目录时必须使用 `git mv` 以保留 git 历史。

若 `raw/` 目录结构调整，可使用脚本自动迁移并同步更新所有 wiki 页面中的路径引用：

```bash
# 先预览
python scripts/migrate-raw.py --dry-run "旧路径" "新路径"

# 正式执行
python scripts/migrate-raw.py "旧路径" "新路径"
```

该脚本会执行 `git mv` 移动目录，并自动扫描更新 `wiki/` 和 `CLAUDE.md` 中的：
- Markdown 链接（`../../raw/...`）
- 正文中的 `raw/...` 文本引用
- YAML frontmatter `sources` 列表

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

## 开发环境

- Python 虚拟环境位于 `pythonenv/bin/activate`，处理 Excel/docx 等资料时可先激活该环境。
- **运行 `bot/` 代码前必须激活虚拟环境**：`source /root/llm-wiki/pythonenv/bin/activate`，否则 `google-adk` 等依赖会报 `ModuleNotFoundError`。
- **Bot 本地启动**（在 `bot/` 目录下）：`python main.py`（默认 `127.0.0.1:8080`）；自定义端口/地址用 `PORT=8804 ADK_API_HOST=0.0.0.0 python main.py`。
- **Bot Docker 启动**：镜像构建后，将宿主机的 `wiki/` 和 `site/` 挂载到容器根目录的 `/wiki` 和 `/site`（`wiki_tools.py` 会优先查找这两个绝对路径），无需额外环境变量。

### Bot 服务架构

- `rag-skill` 采用**工具驱动检索**：`search_wiki` 找文件 → `read_wiki_page` 读内容，不依赖静态 `<files>` 引用（wiki+site 总量超 1MB，无法放入上下文）。
- `SKILL.md` 的 `external_references` 字段由 `skill_loader.py` **自定义加载**，非 ADK 原生功能；外部目录的文本文件会被读取为 Skill 的 references。
- `site/` 下的 `index.html` 是聚合页，搜索排序时** wiki 文件优先级高于 site**，避免聚合页抢占相关结果。

## 当前状态

- 第一批资料已摄入（3 份会议记录）。
- 第二批资料已摄入（AI 芯片竞品分析资料：NVIDIA/华为/寒武纪/燧原等）。
- 第三批资料已摄入（亿铸科技中移动展会 Q&A）。
- Wiki 页面数：40（5 source + 20 entity + 13 concept + index + log + overview）。

## 设计参考

- UI 设计统一参考 [`DESIGN.md`](DESIGN.md) 中的 Apple 风格设计系统。

## 站点构建

- 构建命令：`python scripts/build_site.py`（输出 `site/index.html`，单页应用）
- 测试命令：`python -m pytest scripts/tests/ -v`
- 本地预览：`python -m http.server 8800 --directory site/`（修改模板后需重建并重启服务才能生效）
- 构建产物：`site/index.html` 为单页应用，内含所有页面数据；`site/raw` 为符号链接，确保原始文件可下载
- 样式与路由模板位于 `scripts/build_site/assets.py` 的 `SITE_TEMPLATE` 中；`renderer.py` 会在构建时将项目根目录 `assets/` 复制到 `site/assets/`
- 页面布局网格为 `280px 1fr 260px`（左导航 / 内容区 / 右目录），修改整体宽度或新增侧边面板时需同步更新 `.layout` 的 `grid-template-columns`

## 工具命令

- `/plugin`: 用于调用插件扩展功能。
