"""Wiki / Site 检索工具：支持按关键词搜索和按路径读取页面内容。

运行时从环境变量或相对路径定位 wiki/site 目录；
未来 Docker 启动时通过挂载将外部 wiki/site 映射到容器内同一相对位置即可。
"""
from __future__ import annotations

import os
import pathlib
import re
from typing import Any


def _repo_root() -> pathlib.Path:
    """定位项目根目录（bot/ 的父目录）。"""
    return pathlib.Path(__file__).resolve().parent.parent.parent.parent


def _wiki_dir() -> pathlib.Path:
    p = os.environ.get("RAG_WIKI_PATH", "")
    if p:
        return pathlib.Path(p).resolve()
    root_wiki = _repo_root() / "wiki"
    if root_wiki.is_dir():
        return root_wiki
    # Docker 中若 wiki 挂载在 bot/ 同级或 bot/ 内部，兜底
    return pathlib.Path(__file__).resolve().parent.parent.parent / "wiki"


def _site_dir() -> pathlib.Path:
    p = os.environ.get("RAG_SITE_PATH", "")
    if p:
        return pathlib.Path(p).resolve()
    root_site = _repo_root() / "site"
    if root_site.is_dir():
        return root_site
    return pathlib.Path(__file__).resolve().parent.parent.parent / "site"


def _is_text_file(path: pathlib.Path) -> bool:
    """通过扩展名和试读判断是否为文本文件。"""
    text_exts = {".md", ".txt", ".html", ".htm", ".json", ".yaml", ".yml", ".css", ".js"}
    if path.suffix.lower() in text_exts:
        return True
    try:
        path.read_text(encoding="utf-8")
        return True
    except (UnicodeDecodeError, IOError):
        return False


def _extract_title(content: str, path: pathlib.Path) -> str:
    """从 Markdown/YAML frontmatter 或 HTML title 中提取标题。"""
    # YAML frontmatter
    if content.lstrip().startswith("---"):
        m = re.search(r"^title:\s*(.+)$", content, re.MULTILINE)
        if m:
            return m.group(1).strip()
    # Markdown H1
    m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # HTML title
    m = re.search(r"<title[^>]*>(.+?)</title>", content, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return path.stem


def _strip_html_tags(html: str) -> str:
    """简单去除 HTML 标签并规范化空白。"""
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&\w+;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _read_content(path: pathlib.Path, max_chars: int = 8000) -> str:
    """读取文件内容；HTML 会做简单文本提取。"""
    try:
        raw = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, IOError):
        return ""
    if path.suffix.lower() in {".html", ".htm"}:
        raw = _strip_html_tags(raw)
    return raw[:max_chars]


def _build_index() -> list[dict[str, Any]]:
    """扫描 wiki/ 与 site/ 目录，构建文件索引。"""
    index: list[dict[str, Any]] = []
    for base_dir in (_wiki_dir(), _site_dir()):
        if not base_dir.is_dir():
            continue
        for path in sorted(base_dir.rglob("*")):
            if not path.is_file() or not _is_text_file(path):
                continue
            rel = path.relative_to(base_dir).as_posix()
            content = _read_content(path, max_chars=4000)
            title = _extract_title(content, path)
            index.append({
                "category": base_dir.name,
                "path": f"{base_dir.name}/{rel}",
                "absolute_path": str(path),
                "title": title,
                "snippet": content[:300].replace("\n", " "),
            })
    return index


# 模块级缓存（进程生命周期内只扫描一次）
_index_cache: list[dict[str, Any]] | None = None


def _get_index() -> list[dict[str, Any]]:
    global _index_cache
    if _index_cache is None:
        _index_cache = _build_index()
    return _index_cache


def search_wiki(keywords: str, top_k: int = 5) -> str:
    """在 wiki 与 site 中搜索与关键词相关的页面。

    Args:
        keywords: 用户问题的核心关键词，多个词可用空格分隔。
        top_k: 返回的最相关结果数量（默认 5）。

    Returns:
        JSON 格式的搜索结果列表字符串。
    """
    import json

    if not keywords or not keywords.strip():
        return json.dumps({"error": "关键词不能为空"}, ensure_ascii=False)

    terms = [t.lower() for t in keywords.strip().split() if t.strip()]
    if not terms:
        return json.dumps({"error": "关键词不能为空"}, ensure_ascii=False)

    index = _get_index()
    scored: list[tuple[int, dict[str, Any]]] = []
    for item in index:
        text = f"{item['title']} {item['path']} {item['snippet']}".lower()
        score = sum(2 if t in item["title"].lower() else 1 for t in terms if t in text)
        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda x: (-x[0], 0 if x[1]["category"] == "wiki" else 1, x[1]["path"]))
    results = [
        {
            "path": item["path"],
            "title": item["title"],
            "snippet": item["snippet"][:200] + "..." if len(item["snippet"]) > 200 else item["snippet"],
        }
        for _, item in scored[:top_k]
    ]

    return json.dumps({"results": results, "total": len(scored)}, ensure_ascii=False)


def read_wiki_page(path: str) -> str:
    """读取指定路径的 wiki/site 页面完整内容。

    Args:
        path: 页面路径，格式为 `wiki/xxx.md` 或 `site/xxx.html`，
              也可以是 search_wiki 返回的 `path` 字段。

    Returns:
        页面文本内容（HTML 已做简单标签去除）。
    """
    repo = _repo_root()
    # 支持多种路径格式
    possible_paths = [
        repo / path,
        pathlib.Path(path),
    ]
    # 如果是 wiki/xxx.md 或 site/xxx.html 格式，也尝试从环境变量目录找
    if path.startswith("wiki/"):
        possible_paths.insert(0, _wiki_dir() / path[5:])
    elif path.startswith("site/"):
        possible_paths.insert(0, _site_dir() / path[5:])

    for p in possible_paths:
        p = p.resolve()
        # 安全检查：防止目录遍历
        try:
            p.relative_to(_wiki_dir())
        except ValueError:
            try:
                p.relative_to(_site_dir())
            except ValueError:
                try:
                    p.relative_to(repo)
                except ValueError:
                    continue
        if p.is_file() and _is_text_file(p):
            content = _read_content(p, max_chars=50000)
            return content

    return f"错误：未找到可读的文本文件：{path}。请先用 search_wiki 确认文件路径。"
