from __future__ import annotations

from pathlib import Path

import pytest

from docsmoke.config import Config, load
from docsmoke.exceptions import ConfigError


def test_load_defaults_without_config(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)

    config = load()

    assert config == Config(project_root=tmp_path)


def test_load_docsmoke_toml(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docsmoke.toml").write_text(
        'include = ["guides/**/*.md"]\ndefault_timeout = 3.5\nfail_fast = true\n',
        encoding="utf-8",
    )

    config = load()

    assert config.project_root == tmp_path
    assert config.include == ("guides/**/*.md",)
    assert config.default_timeout == 3.5
    assert config.fail_fast is True


def test_load_pyproject_section(tmp_path) -> None:
    path = tmp_path / "pyproject.toml"
    path.write_text(
        "[tool.docsmoke]\ninclude = ['docs/*.md']\nrequire_directive = false\n",
        encoding="utf-8",
    )

    config = load(path)

    assert config.include == ("docs/*.md",)
    assert config.require_directive is False


def test_invalid_timeout_raises_config_error(tmp_path) -> None:
    path = tmp_path / "docsmoke.toml"
    path.write_text("default_timeout = 'fast'\n", encoding="utf-8")

    with pytest.raises(ConfigError):
        load(path)


def test_missing_config_file_raises(tmp_path) -> None:
    with pytest.raises(ConfigError):
        load(tmp_path / "missing.toml")


def test_config_validates_positive_timeout() -> None:
    with pytest.raises(ConfigError):
        Config(project_root=Path.cwd(), default_timeout=0)


def test_config_validates_non_empty_include() -> None:
    with pytest.raises(ConfigError):
        Config(project_root=Path.cwd(), include=())


def test_config_validates_include_item_types() -> None:
    with pytest.raises(ConfigError):
        Config(project_root=Path.cwd(), include=("",))


def test_config_validates_exclude_item_types() -> None:
    with pytest.raises(ConfigError):
        Config(project_root=Path.cwd(), exclude=("",))


def test_load_rejects_invalid_boolean_values(tmp_path) -> None:
    path = tmp_path / "docsmoke.toml"
    path.write_text("fail_fast = 'no'\n", encoding="utf-8")

    with pytest.raises(ConfigError):
        load(path)


def test_load_rejects_invalid_require_directive_value(tmp_path) -> None:
    path = tmp_path / "docsmoke.toml"
    path.write_text("require_directive = 'yes'\n", encoding="utf-8")

    with pytest.raises(ConfigError):
        load(path)


def test_load_rejects_non_list_include(tmp_path) -> None:
    path = tmp_path / "docsmoke.toml"
    path.write_text("include = 42\n", encoding="utf-8")

    with pytest.raises(ConfigError):
        load(path)


def test_load_rejects_invalid_include_items(tmp_path) -> None:
    path = tmp_path / "docsmoke.toml"
    path.write_text("include = ['README.md', '']\n", encoding="utf-8")

    with pytest.raises(ConfigError):
        load(path)


def test_load_accepts_string_include(tmp_path) -> None:
    path = tmp_path / "docsmoke.toml"
    path.write_text("include = 'guides/*.md'\n", encoding="utf-8")

    config = load(path)

    assert config.include == ("guides/*.md",)


def test_load_rejects_invalid_docsmoke_section(tmp_path) -> None:
    path = tmp_path / "pyproject.toml"
    path.write_text("[tool]\ndocsmoke = 'bad'\n", encoding="utf-8")

    with pytest.raises(ConfigError):
        load(path)
