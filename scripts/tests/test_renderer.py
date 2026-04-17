import json
from pathlib import Path

from build_site.assets import SITE_TEMPLATE
from build_site.renderer import render_site_html


class TestAssets:
    def test_template_has_placeholders(self):
        assert "{{nav_html}}" in SITE_TEMPLATE
        assert "{{pages_json}}" in SITE_TEMPLATE

    def test_template_contains_apple_css(self):
        assert "--bg-light: #f5f5f7" in SITE_TEMPLATE
        assert "--apple-blue: #0071e3" in SITE_TEMPLATE
        assert "backdrop-filter: saturate(180%) blur(20px)" in SITE_TEMPLATE


class TestRenderer:
    def test_render_site_html_creates_file(self, tmp_path: Path):
        nav = '<a href="#/wiki/test.md">test.md</a>'
        pages = {
            "wiki/test.md": {
                "title": "Test",
                "type": "wiki",
                "html": "<h1>Test</h1>",
                "toc": [{"id": "test", "name": "Test", "children": []}],
            }
        }
        output = tmp_path / "index.html"
        render_site_html(nav, pages, str(output))
        assert output.exists()
        content = output.read_text(encoding="utf-8")
        assert "LLM Wiki" in content
        assert nav in content
        assert json.dumps(pages, ensure_ascii=False) in content

    def test_pages_json_serializable(self, tmp_path: Path):
        pages = {
            "wiki/a.md": {
                "title": "A",
                "type": "wiki",
                "html": "<p>A</p>",
                "toc": [],
            }
        }
        output = tmp_path / "index.html"
        render_site_html("", pages, str(output))
        content = output.read_text(encoding="utf-8")
        assert '"title": "A"' in content
