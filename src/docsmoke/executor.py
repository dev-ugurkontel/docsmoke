"""Snippet execution primitives."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from pathlib import Path

from docsmoke.models import Snippet, SnippetResult, SnippetStatus


def run_snippet(snippet: Snippet, *, project_root: Path, default_timeout: float) -> SnippetResult:
    """Execute a single snippet and evaluate its expectations."""
    if snippet.directives.skip:
        return SnippetResult(
            snippet=snippet,
            status=SnippetStatus.skipped,
            duration_seconds=0.0,
            exit_code=None,
            stdout="",
            stderr="",
            message="snippet marked as skipped",
        )

    if not snippet.code.strip():
        return SnippetResult(
            snippet=snippet,
            status=SnippetStatus.error,
            duration_seconds=0.0,
            exit_code=None,
            stdout="",
            stderr="",
            message="snippet body is empty",
        )

    timeout = snippet.directives.timeout or default_timeout
    cwd = _resolve_cwd(project_root, snippet)
    if not cwd.exists():
        return SnippetResult(
            snippet=snippet,
            status=SnippetStatus.error,
            duration_seconds=0.0,
            exit_code=None,
            stdout="",
            stderr="",
            message=f"working directory does not exist: {cwd}",
        )
    if not cwd.is_dir():
        return SnippetResult(
            snippet=snippet,
            status=SnippetStatus.error,
            duration_seconds=0.0,
            exit_code=None,
            stdout="",
            stderr="",
            message=f"working directory is not a directory: {cwd}",
        )
    env = os.environ.copy()
    env["PATH"] = _prepend_executable_dir(env.get("PATH", ""))
    env.update(snippet.directives.env)
    command = _build_command(snippet)

    started = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        duration = time.perf_counter() - started
        return SnippetResult(
            snippet=snippet,
            status=SnippetStatus.error,
            duration_seconds=duration,
            exit_code=None,
            stdout="",
            stderr="",
            message=f"executor not available: {exc.filename}",
        )
    except subprocess.TimeoutExpired as exc:
        duration = time.perf_counter() - started
        return SnippetResult(
            snippet=snippet,
            status=SnippetStatus.error,
            duration_seconds=duration,
            exit_code=None,
            stdout=_coerce_output(exc.stdout),
            stderr=_coerce_output(exc.stderr),
            message=f"timed out after {timeout:.1f}s",
        )

    duration = time.perf_counter() - started
    status, message = _evaluate(snippet, completed.returncode, completed.stdout, completed.stderr)
    return SnippetResult(
        snippet=snippet,
        status=status,
        duration_seconds=duration,
        exit_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        message=message,
    )


def _build_command(snippet: Snippet) -> list[str]:
    if snippet.executor == "python":
        return [sys.executable, "-c", snippet.code]
    return [snippet.directives.shell or snippet.executor, "-eu", "-c", snippet.code]


def _resolve_cwd(project_root: Path, snippet: Snippet) -> Path:
    if snippet.directives.cwd is None:
        return project_root
    return (project_root / snippet.directives.cwd).resolve()


def _evaluate(
    snippet: Snippet,
    exit_code: int,
    stdout: str,
    stderr: str,
) -> tuple[SnippetStatus, str]:
    if exit_code != 0:
        return SnippetStatus.failed, f"snippet exited with code {exit_code}"

    combined = stdout + stderr
    for expected in snippet.directives.expect_contains:
        if expected not in combined:
            return SnippetStatus.failed, f"missing expected text: {expected!r}"

    for pattern in snippet.directives.expect_regex:
        try:
            matched = re.search(pattern, combined, flags=re.MULTILINE)
        except re.error as exc:
            return SnippetStatus.error, f"invalid regex {pattern!r}: {exc}"
        if matched is None:
            return SnippetStatus.failed, f"missing regex match: {pattern!r}"

    return SnippetStatus.passed, "ok"


def _coerce_output(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return value


def _prepend_executable_dir(path_value: str) -> str:
    executable_dir = Path(sys.executable).parent
    if path_value:
        return f"{executable_dir}{os.pathsep}{path_value}"
    return str(executable_dir)
