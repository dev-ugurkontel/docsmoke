from __future__ import annotations

from pathlib import Path

from docsmoke.executor import run_snippet
from docsmoke.models import Snippet, SnippetDirectives, SnippetStatus


def _snippet(*, language: str, executor: str, code: str, directives: SnippetDirectives) -> Snippet:
    return Snippet(
        path=Path("README.md"),
        language=language,
        executor=executor,
        code=code,
        start_line=1,
        end_line=3,
        directives=directives,
    )


def test_run_shell_snippet_success(tmp_path) -> None:
    snippet = _snippet(
        language="bash",
        executor="sh",
        code="printf 'hello\\n'",
        directives=SnippetDirectives(expect_contains=("hello",)),
    )

    result = run_snippet(snippet, project_root=tmp_path, default_timeout=5.0)

    assert result.status is SnippetStatus.passed
    assert result.exit_code == 0


def test_run_shell_snippet_fails_on_missing_expectation(tmp_path) -> None:
    snippet = _snippet(
        language="bash",
        executor="sh",
        code="printf 'hello\\n'",
        directives=SnippetDirectives(expect_contains=("goodbye",)),
    )

    result = run_snippet(snippet, project_root=tmp_path, default_timeout=5.0)

    assert result.status is SnippetStatus.failed
    assert "missing expected text" in result.message


def test_run_python_snippet_with_env(tmp_path) -> None:
    snippet = _snippet(
        language="python",
        executor="python",
        code="import os; print(os.environ['DOCSMOKE_TEST'])",
        directives=SnippetDirectives(env={"DOCSMOKE_TEST": "ok"}, expect_contains=("ok",)),
    )

    result = run_snippet(snippet, project_root=tmp_path, default_timeout=5.0)

    assert result.status is SnippetStatus.passed
    assert "ok" in result.stdout


def test_skipped_snippet_does_not_execute(tmp_path) -> None:
    snippet = _snippet(
        language="bash",
        executor="sh",
        code="exit 1",
        directives=SnippetDirectives(skip=True),
    )

    result = run_snippet(snippet, project_root=tmp_path, default_timeout=5.0)

    assert result.status is SnippetStatus.skipped
    assert result.exit_code is None


def test_empty_snippet_is_reported_as_error(tmp_path) -> None:
    snippet = _snippet(
        language="bash",
        executor="sh",
        code="",
        directives=SnippetDirectives(),
    )

    result = run_snippet(snippet, project_root=tmp_path, default_timeout=5.0)

    assert result.status is SnippetStatus.error


def test_timeout_is_reported_as_error(tmp_path) -> None:
    snippet = _snippet(
        language="python",
        executor="python",
        code="import time; time.sleep(0.05)",
        directives=SnippetDirectives(),
    )

    result = run_snippet(snippet, project_root=tmp_path, default_timeout=0.001)

    assert result.status is SnippetStatus.error
    assert "timed out" in result.message


def test_missing_shell_is_reported_as_error(tmp_path) -> None:
    snippet = _snippet(
        language="bash",
        executor="sh",
        code="printf 'hello\\n'",
        directives=SnippetDirectives(shell="definitely-not-a-shell"),
    )

    result = run_snippet(snippet, project_root=tmp_path, default_timeout=5.0)

    assert result.status is SnippetStatus.error
    assert "executor not available" in result.message


def test_regex_expectation_failure(tmp_path) -> None:
    snippet = _snippet(
        language="bash",
        executor="sh",
        code="printf 'hello\\n'",
        directives=SnippetDirectives(expect_regex=(r"world\d+",)),
    )

    result = run_snippet(snippet, project_root=tmp_path, default_timeout=5.0)

    assert result.status is SnippetStatus.failed
    assert "regex" in result.message


def test_cwd_is_resolved_from_project_root(tmp_path) -> None:
    working_dir = tmp_path / "nested"
    working_dir.mkdir()
    snippet = _snippet(
        language="bash",
        executor="sh",
        code="pwd",
        directives=SnippetDirectives(cwd="nested", expect_contains=(str(working_dir),)),
    )

    result = run_snippet(snippet, project_root=tmp_path, default_timeout=5.0)

    assert result.status is SnippetStatus.passed


def test_executor_prepends_current_python_bin_to_path(tmp_path) -> None:
    snippet = _snippet(
        language="bash",
        executor="sh",
        code="docsmoke --version",
        directives=SnippetDirectives(expect_contains=("docsmoke 0.1.0",)),
    )

    result = run_snippet(snippet, project_root=tmp_path, default_timeout=5.0)

    assert result.status is SnippetStatus.passed
