import tempfile
from pathlib import Path

import pytest

from build_site.parser import parse_frontmatter, read_wiki_page, read_raw_file


class TestParseFrontmatter:
    def test_valid_frontmatter(self):
        content = """---
title: Test Page
type: concept
date: 2024-01-01
---
# Hello
"""
        from datetime import date
        fm, body = parse_frontmatter(content)
        assert fm["title"] == "Test Page"
        assert fm["type"] == "concept"
        assert fm["date"] == date(2024, 1, 1)
        assert body.strip() == "# Hello"

    def test_missing_frontmatter(self):
        content = "# Hello\n\nThis is a test."
        fm, body = parse_frontmatter(content)
        assert fm == {}
        assert body == content

    def test_invalid_yaml_returns_empty(self):
        content = "---\nnot yaml: [\n---\n# Hello"
        fm, body = parse_frontmatter(content)
        assert fm == {}
        assert body == content


class TestReadWikiPage:
    def test_wiki_page_with_frontmatter(self, tmp_path: Path):
        f = tmp_path / "test.md"
        f.write_text(
            "---\ntitle: Wiki Page\ntype: source\n---\n# Heading\n\nParagraph.",
            encoding="utf-8",
        )
        page = read_wiki_page(str(f), "source/test.md")
        assert page["title"] == "Wiki Page"
        assert page["type"] == "wiki"
        assert page["rel_path"] == "source/test.md"
        assert '<h1 id="heading">Heading</h1>' in page["html"]
        assert page["frontmatter"]["type"] == "source"
        assert any(t["name"] == "Heading" for t in page["toc"])

    def test_wiki_page_without_frontmatter(self, tmp_path: Path):
        f = tmp_path / "test.md"
        f.write_text("# Title\n\nBody.", encoding="utf-8")
        page = read_wiki_page(str(f), "test.md")
        assert page["title"] == "test.md"
        assert '<h1 id="title">Title</h1>' in page["html"]


class TestReadRawFile:
    def test_raw_markdown(self, tmp_path: Path):
        f = tmp_path / "note.md"
        f.write_text("# Note\n\nContent.", encoding="utf-8")
        page = read_raw_file(str(f), "02-市场情报/note.md")
        assert page["title"] == "note.md"
        assert page["type"] == "raw"
        assert page["download"] is True
        assert '<h1 id="note">Note</h1>' in page["html"]

    def test_raw_binary_shows_download_card(self, tmp_path: Path):
        f = tmp_path / "data.png"
        f.write_bytes(b"\x89PNG\r\n\x1a\n")
        page = read_raw_file(str(f), "02-市场情报/data.png")
        assert page["title"] == "data.png"
        assert page["download"] is True
        assert "下载文件" in page["html"]
        assert '../raw/02-市场情报/data.png' in page["html"]
        assert page["toc"] == []

    def test_raw_pdf(self, tmp_path: Path):
        f = tmp_path / "doc.pdf"
        f.write_bytes(b"%PDF-1.4")
        page = read_raw_file(str(f), "05-竞品分析/doc.pdf")
        assert page["title"] == "doc.pdf"
        assert "下载文件" in page["html"]
