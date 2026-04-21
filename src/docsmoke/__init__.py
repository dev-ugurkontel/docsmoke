"""docsmoke public package metadata."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

__all__ = ["__version__"]

try:
    __version__ = version("docsmoke")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+unknown"
