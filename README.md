# reascript-mcp

MCP server exposing Reaper/ReaScript project-control helpers to AI agents.

This is the first working slice of the Reaper layer for the Asian Sentry agentic music tooling stack. It complements `music21-mcp`: music21 handles symbolic music reasoning; ReaScript handles project-level DAW control and state readback.

## Current tools

| Tool | What it does |
|------|-------------|
| `parse_rpp_project` | Parse a `.rpp` Reaper project file into compact JSON: tempo, time signature, track names, item counts, and media source types. Works without Reaper installed. |
| `generate_reascript` | Generate Lua ReaScripts for supported actions. Initial actions: `list_tracks` and `create_midi_item`. |

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

Current status: 9 tests passing.

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
```

## Next build slices

1. Add a runner that writes generated Lua files to disk.
2. Add more project-control scripts: create tracks, rename tracks, import MIDI, set tempo map, add markers/regions.
3. Add structured state readback scripts for items, takes, MIDI notes, markers, routing, and FX chains.
4. Connect this to the common musical data model so music21/mido/ReaScript reference the same musical locations.
