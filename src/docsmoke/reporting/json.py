"""JSON report rendering."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from docsmoke.models import ScanReport


def render_json(report: ScanReport) -> str:
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
