# reascript-mcp TODO

Status: active, remote-capable workstream. Audio device is not required for most current tasks.

## Done

- [x] Project scaffold with editable Python package and local venv
- [x] `parse_rpp_project` pure tool for `.rpp` state readback
- [x] `generate_reascript` pure tool for Lua script generation
- [x] `write_reascript_file` pure tool for writing generated Lua scripts to disk
- [x] FastMCP wrapper exposing the current tools
- [x] README with install, run, and usage examples
- [x] Local validation: Python tests green, REAPER binary present, SWS and ReaPack plugins present

## Next: can progress remotely

- [ ] Add Reaper CLI smoke harness that runs against a disposable config/project and exits cleanly
- [ ] Add generated script action: `create_track`
- [ ] Add generated script action: `rename_track`
- [ ] Add generated script action: `add_marker`
- [ ] Add generated script action: `add_region`
- [ ] Add generated script action: `import_midi_file`
- [x] Add state readback script: initial `read_project_state` for tempo, track names, FX chains, media items, and markers/regions
- [ ] Add state readback script: list MIDI notes in selected/all MIDI items
- [ ] Add state readback script: list markers and regions
- [ ] Add state readback script: list routing and sends
- [ ] Add state readback script: list FX chains and parameter values
- [ ] Define JSON schemas for generated script inputs/outputs
- [ ] Add Claude Desktop / Cursor MCP config examples with absolute Mac mini paths

## Requires local/GUI Reaper validation

- [ ] Load generated `list_tracks.lua` in REAPER and verify JSON output
- [ ] Load generated `create_midi_item.lua` in REAPER and verify MIDI item appears on target track
- [ ] Save a small canonical smoke-test `.rpp` for repeated manual testing
- [ ] Validate generated scripts with a real audio interface attached, if any render/playback behaviour is added later

## Larger roadmap links

- Main vault roadmap: `01 - Projects/Music/Research/Music Tooling Roadmap.md`
- Main vault task list: `Tasks.md` → `Music / Asian Sentry`
