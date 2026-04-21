from __future__ import annotations

import pytest

from docsmoke.exceptions import DirectiveError
from docsmoke.markdown import discover_snippets


def test_discover_snippet_with_directives(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "\n".join(
            [
                "```bash docsmoke",
                "# docsmoke: name=quickstart; expect-contains=hello",
                "printf 'hello\\n'",
                "```",
            ]
        ),
        encoding="utf-8",
    )

    snippets = discover_snippets(path)

    assert len(snippets) == 1
    snippet = snippets[0]
    assert snippet.display_name == "quickstart"
    assert snippet.directives.expect_contains == ("hello",)
    assert snippet.code == "printf 'hello\\n'"


def test_expect_contains_can_precede_other_directives(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "\n".join(
            [
                "```bash docsmoke",
                "# docsmoke: expect-contains=hello; name=after-expect",
                "printf 'hello\\n'",
                "```",
            ]
        ),
        encoding="utf-8",
    )

    snippet = discover_snippets(path)[0]

    assert snippet.display_name == "after-expect"
    assert snippet.directives.expect_contains == ("hello",)


def test_discover_snippet_with_cwd_and_regex_directives(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "\n".join(
            [
                "```bash docsmoke",
                "# docsmoke: cwd=examples; expect-regex=hello.+world",
                "printf 'hello world\\n'",
                "```",
            ]
        ),
        encoding="utf-8",
    )

    snippet = discover_snippets(path)[0]

    assert snippet.directives.cwd == "examples"
    assert snippet.directives.expect_regex == ("hello.+world",)


def test_unmarked_snippet_is_ignored_by_default(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text("```bash\nprintf 'hello\\n'\n```\n", encoding="utf-8")

    snippets = discover_snippets(path)

    assert snippets == []


def test_unmarked_snippet_can_be_included(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text("```python\nprint('hello')\n```\n", encoding="utf-8")

    snippets = discover_snippets(path, require_directive=False)

    assert len(snippets) == 1
    assert snippets[0].language == "python"


def test_empty_opted_in_snippet_is_discovered(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text("```bash docsmoke\n```\n", encoding="utf-8")

    snippets = discover_snippets(path)

    assert len(snippets) == 1
    assert snippets[0].code == ""


def test_empty_info_string_is_ignored(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text("```\nplain text\n```\n", encoding="utf-8")

    assert discover_snippets(path, require_directive=False) == []


def test_nested_backtick_examples_are_not_misread_as_snippets(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "\n".join(
            [
                "````markdown",
                "```bash docsmoke",
                "# docsmoke: expect-contains=hello",
                "printf 'hello\\n'",
                "```",
                "````",
            ]
        ),
        encoding="utf-8",
    )

    assert discover_snippets(path) == []


def test_tilde_fences_are_supported(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "~~~python docsmoke\n# docsmoke: name=tilde\nprint('hello')\n~~~\n",
        encoding="utf-8",
    )

    snippets = discover_snippets(path)

    assert len(snippets) == 1
    assert snippets[0].display_name == "tilde"


def test_four_space_indented_fences_are_ignored(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text("    ```bash docsmoke\nprintf 'hello\\n'\n    ```\n", encoding="utf-8")

    assert discover_snippets(path) == []


def test_four_space_indented_closing_markers_remain_body_text(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "\n".join(
            [
                "```bash docsmoke",
                "    ```",
                "printf 'hello\\n'",
                "```",
            ]
        ),
        encoding="utf-8",
    )

    snippet = discover_snippets(path)[0]

    assert snippet.code == "    ```\nprintf 'hello\\n'"


def test_invalid_directive_raises(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "```bash docsmoke\n# docsmoke: timeout=fast\nprintf 'hello\\n'\n```\n", encoding="utf-8"
    )

    with pytest.raises(DirectiveError):
        discover_snippets(path)


def test_non_positive_timeout_directive_raises(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "```bash docsmoke\n# docsmoke: timeout=0\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )

    with pytest.raises(DirectiveError, match="greater than 0"):
        discover_snippets(path)


def test_timeout_can_precede_other_directives(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "```bash docsmoke\n# docsmoke: timeout=1; name=timed\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )

    snippet = discover_snippets(path)[0]

    assert snippet.directives.timeout == 1.0
    assert snippet.display_name == "timed"


def test_html_comment_directives_are_supported(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "```python docsmoke\n<!-- docsmoke: expect-contains=ok -->\nprint('ok')\n```\n",
        encoding="utf-8",
    )

    snippets = discover_snippets(path)

    assert snippets[0].directives.expect_contains == ("ok",)


def test_unknown_directive_raises(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "```bash docsmoke\n# docsmoke: unsupported=yes\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )

    with pytest.raises(DirectiveError):
        discover_snippets(path)


def test_env_and_skip_directives_are_parsed(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "\n".join(
            [
                "```bash docsmoke",
                "# docsmoke: env.NAME=value; skip=false; shell=sh",
                "printf 'hello\\n'",
                "```",
            ]
        ),
        encoding="utf-8",
    )

    snippet = discover_snippets(path)[0]

    assert snippet.directives.env == {"NAME": "value"}
    assert snippet.directives.skip is False
    assert snippet.directives.shell == "sh"


def test_line_comment_and_empty_directive_parts_are_supported(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "\n".join(
            [
                "```bash docsmoke",
                "// docsmoke: name=line-comment;; skip",
                "printf 'hello\\n'",
                "```",
            ]
        ),
        encoding="utf-8",
    )

    snippet = discover_snippets(path)[0]

    assert snippet.display_name == "line-comment"
    assert snippet.directives.skip is True


def test_invalid_boolean_directive_raises(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "```bash docsmoke\n# docsmoke: skip=maybe\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )

    with pytest.raises(DirectiveError):
        discover_snippets(path)


def test_directive_without_value_raises(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "```bash docsmoke\n# docsmoke: timeout=\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )

    with pytest.raises(DirectiveError):
        discover_snippets(path)


def test_empty_env_name_raises(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text(
        "```bash docsmoke\n# docsmoke: env.=value\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )

    with pytest.raises(DirectiveError):
        discover_snippets(path)


def test_unsupported_language_is_ignored(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text("```ruby docsmoke\nputs 'hello'\n```\n", encoding="utf-8")

    assert discover_snippets(path) == []


def test_unclosed_fence_uses_last_line_as_end(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text("```bash docsmoke\nprintf 'hello\\n'\n", encoding="utf-8")

    snippet = discover_snippets(path)[0]

    assert snippet.end_line == 2
