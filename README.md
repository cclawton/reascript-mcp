# reascript-mcp

MCP server exposing Reaper/ReaScript project-control helpers to AI agents.

This is the first working slice of the Reaper layer for the Asian Sentry agentic music tooling stack. It complements `music21-mcp`: music21 handles symbolic music reasoning; ReaScript handles project-level DAW control and state readback.

## Current tools

| Tool | What it does |
|------|-------------|
| `parse_rpp_project` | Parse a `.rpp` Reaper project file into compact JSON: tempo, time signature, track names, item counts, and media source types. Works without Reaper installed. |
| `generate_reascript` | Generate Lua ReaScripts for supported actions. Current actions: `list_tracks`, `read_project_state`, `create_track`, `create_midi_item`, and `import_midi_file`. |
| `write_reascript_file` | Generate a supported Lua ReaScript and write it to disk for loading/running in REAPER. |

## Install

```bash
cd reascript-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## Run tests

```bash
python -m pytest -q
```

Current status: 12 tests passing.

## Use as MCP server

```bash
python -m reascript_mcp.server
```

Example MCP config:

```json
{
  "mcpServers": {
    "reascript-mcp": {
      "command": "/path/to/reascript-mcp/.venv/bin/python",
      "args": ["-m", "reascript_mcp.server"],
      "cwd": "/path/to/reascript-mcp"
    }
  }
}
```

## Direct Python examples

```python
from reascript_mcp.tools.parse_rpp_project import parse_rpp_project
from reascript_mcp.tools.generate_reascript import generate_reascript

print(parse_rpp_project("song.rpp"))

script = generate_reascript("list_tracks", {"output_path": "tracks.json"})
print(script["script"])

from reascript_mcp.tools.write_reascript_file import write_reascript_file
write_reascript_file("list_tracks", {"output_path": "tracks.json"})
```

## Next build slices

1. Add a Reaper CLI smoke harness that runs against a disposable config/project and exits cleanly.
2. Add more project-control scripts: create tracks, rename tracks, import MIDI, set tempo map, add markers/regions.
3. Expand structured state readback scripts beyond `read_project_state`: MIDI note contents, routing/sends, FX parameter snapshots, and render metadata.
4. Connect this to the common musical data model so music21/mido/ReaScript reference the same musical locations.
