"""Data models for docsmoke scans."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class SnippetStatus(str, Enum):
    passed = "passed"
    failed = "failed"
    skipped = "skipped"
    error = "error"


@dataclass(slots=True)
class SnippetDirectives:
    name: str | None = None
    cwd: str | None = None
    timeout: float | None = None
    expect_contains: tuple[str, ...] = ()
    expect_regex: tuple[str, ...] = ()
    env: dict[str, str] = field(default_factory=dict)
    shell: str | None = None
    skip: bool = False


@dataclass(slots=True)
class Snippet:
    path: Path
    language: str
    executor: str
    code: str
    start_line: int
    end_line: int
    directives: SnippetDirectives

    @property
    def display_name(self) -> str:
        return self.directives.name or self.identifier

    @property
    def identifier(self) -> str:
        return f"{self.path}:{self.start_line}"


@dataclass(slots=True)
class SnippetResult:
    snippet: Snippet
    status: SnippetStatus
    duration_seconds: float
    exit_code: int | None
    stdout: str
    stderr: str
    message: str

    def to_dict(self) -> dict[str, object]:
        return {
            "snippet": {
                "id": self.snippet.identifier,
                "name": self.snippet.display_name,
                "path": str(self.snippet.path),
                "language": self.snippet.language,
                "executor": self.snippet.executor,
                "start_line": self.snippet.start_line,
                "end_line": self.snippet.end_line,
            },
            "status": self.status.value,
            "duration_seconds": round(self.duration_seconds, 6),
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "message": self.message,
        }


@dataclass(slots=True)
class ScanReport:
    results: list[SnippetResult] = field(default_factory=list)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime | None = None

    def finish(self) -> None:
        self.finished_at = datetime.now(timezone.utc)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(result.status is SnippetStatus.passed for result in self.results)

    @property
    def failed(self) -> int:
        return sum(result.status is SnippetStatus.failed for result in self.results)

    @property
    def skipped(self) -> int:
        return sum(result.status is SnippetStatus.skipped for result in self.results)

    @property
    def errors(self) -> int:
        return sum(result.status is SnippetStatus.error for result in self.results)

    @property
    def has_failures(self) -> bool:
        return self.failed > 0 or self.errors > 0

    @property
    def duration_seconds(self) -> float:
        finished_at = self.finished_at or self.started_at
        return (finished_at - self.started_at).total_seconds()

    def to_dict(self) -> dict[str, object]:
        return {
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "duration_seconds": round(self.duration_seconds, 6),
            "summary": {
                "total": self.total,
                "passed": self.passed,
                "failed": self.failed,
                "skipped": self.skipped,
                "errors": self.errors,
            },
            "results": [result.to_dict() for result in self.results],
        }
