"""Markdown fenced-block discovery and docsmoke directive parsing."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from docsmoke.exceptions import DirectiveError
from docsmoke.models import Snippet, SnippetDirectives

if TYPE_CHECKING:
    from pathlib import Path

DIRECTIVE_PATTERNS = (
    re.compile(r"^\s*#\s*docsmoke:\s*(?P<body>.+?)\s*$"),
    re.compile(r"^\s*//\s*docsmoke:\s*(?P<body>.+?)\s*$"),
    re.compile(r"^\s*<!--\s*docsmoke:\s*(?P<body>.+?)\s*-->\s*$"),
)

SUPPORTED_EXECUTORS = {
    "bash": "bash",
    "sh": "sh",
    "shell": "sh",
    "zsh": "zsh",
    "python": "python",
    "py": "python",
}


def discover_snippets(path: Path, *, require_directive: bool = True) -> list[Snippet]:
    """Parse a Markdown file and return runnable docsmoke snippets."""
    lines = path.read_text(encoding="utf-8").splitlines()
    snippets: list[Snippet] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.startswith("```"):
            index += 1
            continue

        opening_line = index + 1
        info = line[3:].strip()
        index += 1
        body: list[str] = []
        while index < len(lines) and not lines[index].startswith("```"):
            body.append(lines[index])
            index += 1

        closing_line = index + 1 if index < len(lines) else len(lines)
        language, opted_in = _parse_info_string(info)
        executor = SUPPORTED_EXECUTORS.get(language)

        if executor is None:
            index += 1
            continue

        directives, code, has_directives = _parse_directives(body, path=path, line=opening_line)
        if require_directive and not opted_in and not has_directives:
            index += 1
            continue

        snippets.append(
            Snippet(
                path=path,
                language=language,
                executor=executor,
                code="\n".join(code).rstrip(),
                start_line=opening_line,
                end_line=closing_line,
                directives=directives,
            )
        )
        index += 1

    return snippets


def _parse_info_string(info: str) -> tuple[str, bool]:
    tokens = info.split()
    if not tokens:
        return "", False
    language = tokens[0].lower()
    opted_in = any(token.lower() == "docsmoke" for token in tokens[1:])
    return language, opted_in


def _parse_directives(
    body: list[str],
    *,
    path: Path,
    line: int,
) -> tuple[SnippetDirectives, list[str], bool]:
    directives = SnippetDirectives()
    directive_count = 0
    code = list(body)

    while code:
        payload = _directive_payload(code[0])
        if payload is None:
            break
        directive_count += 1
        _apply_directive_payload(directives, payload, path=path, line=line + directive_count)
        code.pop(0)

    return directives, code, directive_count > 0


def _directive_payload(line: str) -> str | None:
    for pattern in DIRECTIVE_PATTERNS:
        match = pattern.match(line)
        if match:
            return match.group("body")
    return None


def _apply_directive_payload(
    directives: SnippetDirectives,
    payload: str,
    *,
    path: Path,
    line: int,
) -> None:
    for part in payload.split(";"):
        item = part.strip()
        if not item:
            continue
        key, has_sep, value = item.partition("=")
        normalized_key = key.strip().lower()
        normalized_value = value.strip()

        if normalized_key == "name":
            _require_value(has_sep, normalized_value, key=normalized_key, path=path, line=line)
            directives.name = normalized_value
        elif normalized_key == "cwd":
            _require_value(has_sep, normalized_value, key=normalized_key, path=path, line=line)
            directives.cwd = normalized_value
        elif normalized_key == "timeout":
            _require_value(has_sep, normalized_value, key=normalized_key, path=path, line=line)
            try:
                directives.timeout = float(normalized_value)
            except ValueError as exc:
                raise DirectiveError(
                    f"{path}:{line}: timeout must be numeric, got {normalized_value!r}"
                ) from exc
        elif normalized_key == "expect-contains":
            _require_value(has_sep, normalized_value, key=normalized_key, path=path, line=line)
            directives.expect_contains += (normalized_value,)
        elif normalized_key == "expect-regex":
            _require_value(has_sep, normalized_value, key=normalized_key, path=path, line=line)
            directives.expect_regex += (normalized_value,)
        elif normalized_key == "shell":
            _require_value(has_sep, normalized_value, key=normalized_key, path=path, line=line)
            directives.shell = normalized_value
        elif normalized_key == "skip":
            directives.skip = _parse_bool(
                normalized_value if has_sep else "true", path=path, line=line
            )
        elif normalized_key.startswith("env."):
            _require_value(has_sep, normalized_value, key=normalized_key, path=path, line=line)
            env_name = normalized_key[4:]
            if not env_name:
                raise DirectiveError(f"{path}:{line}: env directives require a variable name")
            directives.env[env_name] = normalized_value
        else:
            raise DirectiveError(f"{path}:{line}: unknown docsmoke directive {normalized_key!r}")


def _require_value(has_sep: str, value: str, *, key: str, path: Path, line: int) -> None:
    if has_sep != "=" or value == "":
        raise DirectiveError(f"{path}:{line}: directive {key!r} requires a value")


def _parse_bool(value: str, *, path: Path, line: int) -> bool:
    normalized = value.lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise DirectiveError(f"{path}:{line}: invalid boolean value {value!r}")
