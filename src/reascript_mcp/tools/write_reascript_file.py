"""Write generated Lua ReaScripts to disk for loading/running in Reaper."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .generate_reascript import generate_reascript


def write_reascript_file(
    action: str,
    params: dict[str, Any] | None = None,
    output_dir: str = "generated_reascripts",
    filename: str | None = None,
) -> dict[str, Any]:
    """Generate a supported ReaScript and write it to output_dir.

    output_dir must be a direct directory path, not a path containing '..'. This
    keeps MCP clients from smuggling writes outside the intended script folder.
    """

    params = params or {}
    if ".." in Path(output_dir).parts:
        raise ValueError("output_dir must not contain '..'")

    generated = generate_reascript(action, params)
    safe_filename = filename or Path(generated["script_path"]).name
    if Path(safe_filename).name != safe_filename or not safe_filename.endswith(".lua"):
        raise ValueError("filename must be a simple .lua filename")

    directory = Path(output_dir).expanduser().resolve()
    directory.mkdir(parents=True, exist_ok=True)
    script_path = directory / safe_filename
    script_path.write_text(generated["script"])

    return {
        "action": action,
        "language": generated["language"],
        "script_path": str(script_path),
        "summary": f"Wrote {action} ReaScript to {script_path}",
    }
