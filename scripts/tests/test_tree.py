from pathlib import Path

from build_site.tree import build_wiki_tree, build_raw_trees, flatten_tree, build_nav_html


class TestBuildWikiTree:
    def test_wiki_tree_structure(self, tmp_path: Path):
        wiki = tmp_path / "wiki"
        wiki.mkdir()
        (wiki / "index.md").write_text("# Index", encoding="utf-8")
        (wiki / "concept").mkdir()
        (wiki / "concept" / "fp8.md").write_text("# FP8", encoding="utf-8")

        tree = build_wiki_tree(str(wiki))
        assert tree["name"] == "Wiki"
        assert tree["type"] == "folder"

        # Should have index.md and concept folder
        names = [c["name"] for c in tree["children"]]
        assert "index.md" in names
        assert "concept" in names

        concept = next(c for c in tree["children"] if c["name"] == "concept")
        assert len(concept["children"]) == 1
        assert concept["children"][0]["name"] == "fp8.md"


class TestBuildRawTrees:
    def test_raw_trees_sorted(self, tmp_path: Path):
        raw = tmp_path / "raw"
        raw.mkdir()
        (raw / "02-b").mkdir()
        (raw / "01-a").mkdir()
        (raw / "03-c").mkdir()
        (raw / "02-b" / "file.txt").write_text("hello", encoding="utf-8")
        (raw / "01-a" / "file.txt").write_text("hello", encoding="utf-8")

        trees = build_raw_trees(str(raw))
        names = [t["name"] for t in trees]
        assert names == ["01-a", "02-b", "03-c"]

    def test_raw_tree_excludes_gitkeep(self, tmp_path: Path):
        raw = tmp_path / "raw"
        raw.mkdir()
        (raw / "01-dir").mkdir()
        (raw / "01-dir" / "note.md").write_text("# Note", encoding="utf-8")
        (raw / "01-dir" / ".gitkeep").write_text("", encoding="utf-8")

        trees = build_raw_trees(str(raw))
        folder = trees[0]
        names = [c["name"] for c in folder["children"]]
        assert "note.md" in names
        assert ".gitkeep" not in names


class TestFlattenTree:
    def test_flatten_wiki(self, tmp_path: Path):
        wiki = tmp_path / "wiki"
        wiki.mkdir()
        (wiki / "a.md").write_text("# A", encoding="utf-8")

        tree = build_wiki_tree(str(wiki))
        pages = {}
        flatten_tree(tree["children"], pages, "wiki", str(wiki), str(tmp_path / "raw"))
        assert "wiki/a.md" in pages
        assert pages["wiki/a.md"]["type"] == "wiki"

    def test_flatten_raw(self, tmp_path: Path):
        raw = tmp_path / "raw"
        raw.mkdir()
        (raw / "01-dir").mkdir()
        (raw / "01-dir" / "file.txt").write_text("hello", encoding="utf-8")

        trees = build_raw_trees(str(raw))
        pages = {}
        flatten_tree(trees[0]["children"], pages, "", str(tmp_path / "wiki"), str(raw))
        key = trees[0]["name"] + "/file.txt"
        assert key in pages
        assert pages[key]["type"] == "raw"


class TestBuildNavHtml:
    def test_nav_contains_links(self):
        nodes = [
            {"name": "folder", "type": "folder", "children": [
                {"name": "a.md", "type": "file", "path": "folder/a.md", "source": "/tmp/a.md"}
            ]}
        ]
        html = build_nav_html(nodes, 0, "wiki")
        assert 'href="#/wiki/folder/a.md"' in html
        assert 'data-key="wiki/folder/a.md"' in html
        assert "a.md" in html
        assert 'nav-folder-title' in html

    def test_nav_folder_path_prefix(self):
        nodes = [
            {"name": "Wiki", "type": "folder", "path": "wiki", "children": [
                {"name": "index.md", "type": "file", "path": "index.md", "source": "/tmp/index.md"}
            ]}
        ]
        html = build_nav_html(nodes, 0, "")
        assert 'href="#/wiki/index.md"' in html
        assert 'data-key="wiki/index.md"' in html
