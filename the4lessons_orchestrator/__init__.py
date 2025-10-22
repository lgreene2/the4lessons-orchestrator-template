from __future__ import annotations
import pathlib


def _load_version() -> str:
    """
    Return the project version string.

    Strategy:
    - Prefer a `VERSION` file at the repository root.
    - If not found (e.g., packaged differently), fall back to "0.0.0".
    """
    here = pathlib.Path(__file__).resolve()
    root_version = here.parent.parent / "VERSION"
    if root_version.exists():
        return root_version.read_text(encoding="utf-8").strip()

    local_version = here.parent / "VERSION"
    if local_version.exists():
        return local_version.read_text(encoding="utf-8").strip()

    return "0.0.0"


__version__ = _load_version()
__all__ = ["__version__"]
