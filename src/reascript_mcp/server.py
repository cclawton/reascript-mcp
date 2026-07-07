"""FastMCP server exposing Reaper/ReaScript helper tools."""

from __future__ import annotations

import json
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # Allows pure unit tests without the MCP package installed.
    FastMCP = None  # type: ignore[assignment]

from .tools.generate_reascript import generate_reascript
from .tools.parse_rpp_project import parse_rpp_project
from .tools.write_reascript_file import write_reascript_file

_tool_registry: dict[str, dict[str, Any]] = {
    "parse_rpp_project": {
        "description": "Parse a .rpp Reaper project file into compact JSON state readback.",
        "fn": parse_rpp_project,
    },
    "generate_reascript": {
        "description": "Generate Lua ReaScripts for supported project-control actions.",
        "fn": generate_reascript,
    },
    "write_reascript_file": {
        "description": "Generate and write a Lua ReaScript file for loading/running in Reaper.",
        "fn": write_reascript_file,
    },
}

mcp = FastMCP("reascript-mcp") if FastMCP is not None else None

if mcp is not None:

    @mcp.tool()
    def parse_rpp_project_tool(project_path: str) -> str:
        """Parse a Reaper .rpp project into compact JSON state readback."""

        return json.dumps(parse_rpp_project(project_path), indent=2)

    @mcp.tool()
    def generate_reascript_tool(action: str, params_json: str = "{}") -> str:
        """Generate a Lua ReaScript for a supported action.

        params_json is a JSON object string so MCP clients can pass flexible
        action-specific parameters.
        """

        params = json.loads(params_json)
        if not isinstance(params, dict):
            raise ValueError("params_json must decode to an object")
        return json.dumps(generate_reascript(action, params), indent=2)

    @mcp.tool()
    def write_reascript_file_tool(
        action: str,
        params_json: str = "{}",
        output_dir: str = "generated_reascripts",
        filename: str | None = None,
    ) -> str:
        """Generate a supported Lua ReaScript and write it to disk."""

        params = json.loads(params_json)
        if not isinstance(params, dict):
            raise ValueError("params_json must decode to an object")
        return json.dumps(write_reascript_file(action, params, output_dir, filename), indent=2)


def main() -> None:
    if mcp is None:
        raise RuntimeError("mcp package is not installed. Run: pip install -e .")
    mcp.run()


if __name__ == "__main__":
    main()
