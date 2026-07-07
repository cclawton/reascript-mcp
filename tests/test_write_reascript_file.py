from pathlib import Path

import pytest

from reascript_mcp.tools.write_reascript_file import write_reascript_file


def test_write_reascript_file_creates_lua_file(tmp_path: Path) -> None:
    result = write_reascript_file(
        action="list_tracks",
        params={"output_path": str(tmp_path / "tracks.json")},
        output_dir=str(tmp_path / "scripts"),
    )

    script_path = Path(result["script_path"])
    assert script_path.exists()
    assert script_path.name == "list_tracks.lua"
    assert "reaper.CountTracks(0)" in script_path.read_text()
    assert result["language"] == "lua"
    assert result["summary"].startswith("Wrote")


def test_write_reascript_file_rejects_paths_outside_output_dir(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="output_dir"):
        write_reascript_file(
            action="list_tracks",
            params={},
            output_dir=str(tmp_path / "scripts" / ".." / "elsewhere"),
        )


def test_write_reascript_file_allows_custom_filename(tmp_path: Path) -> None:
    result = write_reascript_file(
        action="create_midi_item",
        params={
            "track_index": 0,
            "start_qn": 0,
            "end_qn": 2,
            "notes": [{"pitch": 60, "start_qn": 0, "end_qn": 1}],
        },
        output_dir=str(tmp_path),
        filename="smoke_create_midi.lua",
    )

    assert Path(result["script_path"]).name == "smoke_create_midi.lua"
    assert "reaper.MIDI_InsertNote" in Path(result["script_path"]).read_text()
