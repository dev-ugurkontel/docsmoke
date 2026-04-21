from __future__ import annotations

from pathlib import Path

from docsmoke.config import Config
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
