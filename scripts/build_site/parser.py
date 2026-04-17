"""Parse wiki pages and raw files into page data."""

from pathlib import Path

import markdown
import yaml

_md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])


def parse_frontmatter(content: str) -> tuple:
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
                return fm or {}, parts[2]
            except Exception:
                pass
    return {}, content


def read_wiki_page(source_path: str, rel_path: str) -> dict:
    content = Path(source_path).read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    _md.reset()
    html = _md.convert(body)
    toc = _md.toc_tokens
    return {
        "title": fm.get("title", rel_path),
        "type": "wiki",
        "rel_path": rel_path,
        "html": html,
        "toc": toc,
        "frontmatter": fm,
    }


def read_raw_file(source_path: str, rel_path: str) -> dict:
    ext = Path(rel_path).suffix.lower()
    if ext == ".md":
        content = Path(source_path).read_text(encoding="utf-8")
        _md.reset()
        html = _md.convert(content)
        toc = _md.toc_tokens
        return {
            "title": Path(rel_path).name,
            "type": "raw",
            "rel_path": rel_path,
            "html": html,
            "toc": toc,
            "download": True,
        }
    else:
        return {
            "title": Path(rel_path).name,
            "type": "raw",
            "rel_path": rel_path,
            "html": f"""
                <div class="download-card">
                    <h1>{Path(rel_path).name}</h1>
                    <p class="meta">文件路径: <code>{rel_path}</code></p>
                    <a class="btn-primary" href="../raw/{rel_path}" download>下载文件</a>
                </div>
            """,
            "toc": [],
            "download": True,
        }
