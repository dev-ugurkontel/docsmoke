from __future__ import annotations

from pathlib import Path

import pytest

from docsmoke.config import Config
from docsmoke.exceptions import ConfigError
from docsmoke.runner import collect_snippets, scan


def test_collect_snippets_uses_config_include(tmp_path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    readme = docs_dir / "guide.md"
    readme.write_text(
        "```bash docsmoke\n# docsmoke: expect-contains=hello\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )
    config = Config(project_root=tmp_path, include=("docs/*.md",))

    snippets = collect_snippets([], config=config)

    assert len(snippets) == 1
    assert snippets[0].path == readme.resolve()


def test_scan_respects_fail_fast(tmp_path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(
        "\n".join(
            [
                "```bash docsmoke",
                "# docsmoke: expect-contains=missing",
                "printf 'hello\\n'",
                "```",
                "",
                "```bash docsmoke",
                "# docsmoke: expect-contains=world",
                "printf 'world\\n'",
                "```",
            ]
        ),
        encoding="utf-8",
    )
    config = Config(project_root=tmp_path, fail_fast=True)

    report = scan([readme], config=config)

    assert report.total == 1
    assert report.failed == 1


def test_collect_snippets_from_directory_and_excludes_paths(tmp_path) -> None:
    docs_dir = tmp_path / "docs"
    dist_dir = tmp_path / "dist"
    docs_dir.mkdir()
    dist_dir.mkdir()
    (docs_dir / "good.md").write_text(
        "```bash docsmoke\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )
    (dist_dir / "ignored.md").write_text(
        "```bash docsmoke\nprintf 'ignore\\n'\n```\n",
        encoding="utf-8",
    )
    config = Config(project_root=tmp_path, exclude=("dist/**",))

    snippets = collect_snippets([Path()], config=config)

    assert len(snippets) == 1
    assert snippets[0].path.name == "good.md"


def test_collect_snippets_accepts_explicit_markdown_file(tmp_path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("```bash docsmoke\nprintf 'hello\\n'\n```\n", encoding="utf-8")
    config = Config(project_root=tmp_path)

    snippets = collect_snippets([readme], config=config)

    assert len(snippets) == 1
    assert snippets[0].path == readme.resolve()


def test_collect_snippets_ignores_explicit_non_markdown_file(tmp_path) -> None:
    text_file = tmp_path / "README.txt"
    text_file.write_text("```bash docsmoke\nprintf 'hello\\n'\n```\n", encoding="utf-8")
    config = Config(project_root=tmp_path)

    assert collect_snippets([text_file], config=config) == []


def test_collect_snippets_rejects_missing_explicit_path(tmp_path) -> None:
    config = Config(project_root=tmp_path)

    with pytest.raises(ConfigError, match="path does not exist"):
        collect_snippets([Path("missing.md")], config=config)


def test_collect_snippets_ignores_globbed_directories(tmp_path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    config = Config(project_root=tmp_path, include=("docs",))

    assert collect_snippets([], config=config) == []


def test_collect_snippets_does_not_exclude_paths_outside_project(tmp_path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}-outside.md"
    outside.write_text("```bash docsmoke\nprintf 'hello\\n'\n```\n", encoding="utf-8")
    config = Config(project_root=tmp_path)
    try:
        snippets = collect_snippets([outside], config=config)
    finally:
        outside.unlink()

    assert len(snippets) == 1
