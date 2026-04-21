"""File discovery and scan orchestration."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING

from docsmoke.exceptions import ConfigError
from docsmoke.executor import run_snippet
from docsmoke.markdown import discover_snippets
from docsmoke.models import ScanReport, Snippet

if TYPE_CHECKING:
    from docsmoke.config import Config


def collect_snippets(paths: list[Path], *, config: Config) -> list[Snippet]:
    snippets: list[Snippet] = []
    for markdown_file in _resolve_markdown_files(paths, config=config):
        snippets.extend(
            discover_snippets(markdown_file, require_directive=config.require_directive)
        )
    return snippets


def scan(paths: list[Path], *, config: Config) -> ScanReport:
    report = ScanReport()
    for snippet in collect_snippets(paths, config=config):
        result = run_snippet(
            snippet,
            project_root=config.project_root,
            default_timeout=config.default_timeout,
        )
        report.results.append(result)
        if config.fail_fast and result.status.value in {"failed", "error"}:
            break
    report.finish()
    return report


def _resolve_markdown_files(paths: list[Path], *, config: Config) -> list[Path]:
    discovered: set[Path] = set()
    candidates = paths or [Path(pattern) for pattern in config.include]

    if paths:
        for item in candidates:
            resolved = (
                (config.project_root / item).resolve() if not item.is_absolute() else item.resolve()
            )
            if not resolved.exists():
                raise ConfigError(f"path does not exist: {resolved}")
            if resolved.is_dir():
                for child in resolved.rglob("*.md"):
                    if not _is_excluded(child, config=config):
                        discovered.add(child)
            elif resolved.suffix.lower() == ".md" and not _is_excluded(resolved, config=config):
                discovered.add(resolved)
    else:
        for pattern in config.include:
            for child in config.project_root.glob(pattern):
                if (
                    child.is_file()
                    and child.suffix.lower() == ".md"
                    and not _is_excluded(child, config=config)
                ):
                    discovered.add(child.resolve())

    return sorted(discovered)


def _is_excluded(path: Path, *, config: Config) -> bool:
    try:
        relative = PurePosixPath(
            path.resolve().relative_to(config.project_root.resolve()).as_posix()
        )
    except ValueError:
        return False
    return any(relative.match(pattern) for pattern in config.exclude)
