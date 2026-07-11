# reascript-mcp TODO

Status: active, remote-capable workstream. Audio device is not required for most current tasks.

## Done

- [x] Project scaffold with editable Python package and local venv
- [x] `parse_rpp_project` pure tool for `.rpp` state readback
- [x] `parse_rpp_project` extended with FX chains, plugin names, and presets (17 tests)
- [x] `generate_reascript` pure tool for Lua script generation
- [x] `write_reascript_file` pure tool for writing generated Lua scripts to disk
- [x] FastMCP wrapper exposing the current tools (3 MCP tools)
- [x] MCP server registered in Hermes Agent on Mac mini
- [x] README with install, run, and usage examples
- [x] Local validation: Python tests green, REAPER binary present, SWS and ReaPack plugins present
- [x] Local smoke test: Reaper hosted EZdrummer 3, Arturia Analog Lab V, Decent Sampler; render worked; `.rpp` parser and Lua `read_project_state` JSON readback worked

## Architecture: Read/Write Split (updated 2026-07-11)

`.rpp` files are plain text with all project state including MIDI events as `E` lines.

- **Reading**: `parse_rpp_project` is the primary readback tool (offline, fast). Lua read scripts are redundant for offline analysis. Keep `read_project_state` for live verification only.
- **Writing**: Lua/ReaScript for write actions only (create track, insert MIDI, set preset, render).
- **MIDI storage**: Reaper stores MIDI both inline in `.rpp` (`E` lines) and as pooled `.mid` files in `Media/`. The `.mid` files are copies, not live references. Editing them externally likely does NOT update the project. Needs empirical verification.

## Next: can progress remotely

### Offline `.rpp` parser enrichment (read side)
- [ ] Enrich `parse_rpp_project` to parse MIDI `E` lines into structured note data (pitch, velocity, position, channel)
- [ ] Add item position/length parsing to `.rpp` parser (currently only counts items)
- [ ] Parse marker/region data from `.rpp` (currently only via Lua)
- [ ] Parse routing/sends from `.rpp` if present in text format

### Lua write actions (write side only)
- [x] Add generated script action: `create_track`
- [ ] Add generated script action: `rename_track`
- [ ] Add generated script action: `add_marker`
- [ ] Add generated script action: `add_region`
- [x] Add generated script action: `import_midi_file`
- [ ] Add generated script action: `set_track_fx` (load a plugin by name onto a track)
- [ ] Add generated script action: `render_project` (trigger a render with configurable settings)

### MCP server and integration
- [ ] Define JSON schemas for generated script inputs/outputs
- [ ] Add Claude Desktop / Cursor MCP config examples with absolute Mac mini paths
- [ ] Add Reaper CLI smoke harness that runs against a disposable config/project and exits cleanly

## Requires local/GUI Reaper validation

- [x] Load generated `list_tracks.lua` in REAPER and verify JSON output
- [x] Load generated `read_project_state.lua` in REAPER and verify JSON output
- [ ] Load generated `create_midi_item.lua` in REAPER and verify MIDI item appears on target track
- [ ] Save a small canonical smoke-test `.rpp` for repeated manual testing
- [ ] Empirically verify: edit a `.mid` file in `Media/` with music21/mido, reopen project in Reaper, check if changes appear
- [ ] Validate generated scripts with a real audio interface attached, if any render/playback behaviour is added later

## Larger roadmap links

- Main vault roadmap: `01 - Projects/Music/Research/Music Tooling Roadmap.md`
- Main vault task list: `Tasks.md` → `Music / Asian Sentry`
