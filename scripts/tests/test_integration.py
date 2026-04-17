import json
from pathlib import Path

from build_site.tree import build_wiki_tree, build_raw_trees, build_nav_html, flatten_tree
from build_site.renderer import render_site_html


class TestEndToEndBuild:
    def test_full_build(self, tmp_path: Path):
        wiki = tmp_path / "wiki"
        raw = tmp_path / "raw"
        site = tmp_path / "site"
        wiki.mkdir()
        raw.mkdir()

        # Create wiki content
        (wiki / "index.md").write_text("---\ntitle: Home\n---\n# Home\n\nWelcome.", encoding="utf-8")
        (wiki / "concept").mkdir()
        (wiki / "concept" / "test.md").write_text("# Concept", encoding="utf-8")

        # Create raw content
        (raw / "01-资料").mkdir()
        (raw / "01-资料" / "doc.md").write_text("# Doc", encoding="utf-8")
        (raw / "01-资料" / "image.png").write_bytes(b"\x89PNG")

        wiki_tree = build_wiki_tree(str(wiki))
        raw_trees = build_raw_trees(str(raw))

        pages = {}
        flatten_tree(wiki_tree["children"], pages, "wiki", str(wiki), str(raw))
        for t in raw_trees:
            flatten_tree(t["children"], pages, "", str(wiki), str(raw))

        nav_items = []
        if wiki_tree["children"]:
            wiki_tree["path"] = "wiki"
            nav_items.append(build_nav_html([wiki_tree], 0, ""))
        for t in raw_trees:
            if t["children"]:
                nav_items.append(build_nav_html([t], 0, ""))
        nav_html = "".join(nav_items)

        site.mkdir(exist_ok=True)
        output = site / "index.html"
        render_site_html(nav_html, pages, str(output))

        assert output.exists()
        content = output.read_text(encoding="utf-8")
        assert "LLM Wiki" in content
        assert "Home" in content
        assert "wiki/index.md" in content
        assert "01-资料/doc.md" in content
        assert "下载文件" in content

        # Verify raw symlink exists for downloads
        raw_symlink = site / "raw"
        assert raw_symlink.exists() or raw_symlink.is_symlink()
        assert raw_symlink.resolve() == raw.resolve()

        # Verify JSON serializable
        data_start = content.find("const pages = ") + len("const pages = ")
        data_end = content.find(";", data_start)
        pages_data = json.loads(content[data_start:data_end])
        assert "wiki/index.md" in pages_data
        assert pages_data["wiki/index.md"]["title"] == "Home"
