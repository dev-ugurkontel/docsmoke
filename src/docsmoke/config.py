"""Configuration loading and validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from docsmoke.exceptions import ConfigError

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


@dataclass(slots=True)
class Config:
    """User-configurable scan defaults."""

    project_root: Path = field(default_factory=Path.cwd)
    include: tuple[str, ...] = ("README.md", "docs/**/*.md")
    exclude: tuple[str, ...] = (".venv/**", "build/**", "dist/**")
    default_timeout: float = 10.0
    fail_fast: bool = False
    require_directive: bool = True

    def __post_init__(self) -> None:
        if self.default_timeout <= 0:
            raise ConfigError("default_timeout must be greater than 0")
        if not self.include:
            raise ConfigError("include must contain at least one glob")
        if not all(isinstance(item, str) and item for item in self.include):
            raise ConfigError("include must contain non-empty strings")
        if not all(isinstance(item, str) and item for item in self.exclude):
            raise ConfigError("exclude must contain non-empty strings")


def load(config_path: Path | None = None) -> Config:
    """Load configuration from docsmoke.toml or pyproject.toml when present."""
    candidate = config_path
    if candidate is None:
        docsmoke_file = Path.cwd() / "docsmoke.toml"
        pyproject_file = Path.cwd() / "pyproject.toml"
        if docsmoke_file.exists():
            candidate = docsmoke_file
        elif pyproject_file.exists():
            candidate = pyproject_file

    if candidate is None:
        return Config(project_root=Path.cwd())

    if not candidate.exists():
        raise ConfigError(f"config file does not exist: {candidate}")

    data = tomllib.loads(candidate.read_text(encoding="utf-8"))
    source = data if candidate.name == "docsmoke.toml" else data.get("tool", {}).get("docsmoke", {})
    if not isinstance(source, dict):
        raise ConfigError("docsmoke config section must be a TOML table")

    return _from_mapping(source, project_root=candidate.parent)


def _from_mapping(mapping: dict[str, Any], *, project_root: Path) -> Config:
    include = _tuple_of_strings(mapping.get("include", ("README.md", "docs/**/*.md")), "include")
    exclude = _tuple_of_strings(
        mapping.get("exclude", (".venv/**", "build/**", "dist/**")), "exclude"
    )
    default_timeout = mapping.get("default_timeout", 10.0)
    fail_fast = mapping.get("fail_fast", False)
    require_directive = mapping.get("require_directive", True)

    if not isinstance(default_timeout, (int, float)) or isinstance(default_timeout, bool):
        raise ConfigError("default_timeout must be a positive number")
    if not isinstance(fail_fast, bool):
        raise ConfigError("fail_fast must be a boolean")
    if not isinstance(require_directive, bool):
        raise ConfigError("require_directive must be a boolean")

    return Config(
        project_root=project_root.resolve(),
        include=include,
        exclude=exclude,
        default_timeout=float(default_timeout),
        fail_fast=fail_fast,
        require_directive=require_directive,
    )


def _tuple_of_strings(value: Any, field_name: str) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if not isinstance(value, (list, tuple)):
        raise ConfigError(f"{field_name} must be a string or list of strings")
    items = tuple(value)
    if not all(isinstance(item, str) and item for item in items):
        raise ConfigError(f"{field_name} must contain non-empty strings")
    return items
