"""Render the final site HTML."""

import datetime
import json
from pathlib import Path

from build_site.assets import SITE_TEMPLATE


class _DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super().default(obj)


def render_site_html(nav_html: str, pages: dict, output_path: str) -> None:
    output = Path(output_path)
    pages_json = json.dumps(pages, ensure_ascii=False, cls=_DateEncoder)
    html = SITE_TEMPLATE.replace("{{nav_html}}", nav_html).replace("{{pages_json}}", pages_json)
    output.write_text(html, encoding="utf-8")

    # Ensure site/raw symlink exists so raw file downloads work
    site_dir = output.parent
    raw_symlink = site_dir / "raw"
    raw_source = (site_dir.parent / "raw").resolve()
    if not raw_symlink.exists() and raw_source.exists():
        raw_symlink.symlink_to(raw_source, target_is_directory=True)
