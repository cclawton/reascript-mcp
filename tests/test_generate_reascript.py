from pathlib import Path

import pytest

from reascript_mcp.tools.generate_reascript import generate_reascript


def test_generate_list_tracks_script(tmp_path: Path) -> None:
    out = tmp_path / "tracks.json"

    result = generate_reascript("list_tracks", {"output_path": str(out)})

    assert result["language"] == "lua"
    assert result["action"] == "list_tracks"
    assert result["script_path"].endswith("list_tracks.lua")
    assert "reaper.CountTracks(0)" in result["script"]
    assert str(out) in result["script"]
    assert "tracks" in result["summary"]


def test_generate_create_midi_item_script_validates_notes() -> None:
    result = generate_reascript(
        "create_midi_item",
        {
            "track_index": 0,
            "start_qn": 0,
            "end_qn": 4,
            "notes": [
                {"pitch": 60, "start_qn": 0, "end_qn": 1, "velocity": 96},
                {"pitch": 64, "start_qn": 1, "end_qn": 2, "velocity": 88},
            ],
        },
    )

    assert "reaper.MIDI_InsertNote" in result["script"]
    assert "MIDI_GetPPQPosFromProjQN" in result["script"]
    assert "pitch=60" in result["script"]
    assert "2 MIDI notes" in result["summary"]


def test_generate_create_midi_item_rejects_invalid_pitch() -> None:
    with pytest.raises(ValueError, match="pitch"):
        generate_reascript(
            "create_midi_item",
            {
                "track_index": 0,
                "start_qn": 0,
                "end_qn": 1,
                "notes": [{"pitch": 128, "start_qn": 0, "end_qn": 1}],
            },
        )


def test_generate_read_project_state_script_includes_tracks_fx_items_and_markers(tmp_path: Path) -> None:
    out = tmp_path / "project_state.json"

    result = generate_reascript("read_project_state", {"output_path": str(out)})

    assert result["language"] == "lua"
    assert result["action"] == "read_project_state"
    assert result["script_path"].endswith("read_project_state.lua")
    assert str(out) in result["script"]
    assert "reaper.TrackFX_GetCount" in result["script"]
    assert "reaper.TrackFX_GetFXName" in result["script"]
    assert "reaper.CountTrackMediaItems" in result["script"]
    assert "reaper.GetMediaItemInfo_Value" in result["script"]
    assert "reaper.EnumProjectMarkers3" in result["script"]
    assert 'local source_type = reaper.GetMediaSourceType(source, "")' in result["script"]
    assert 'local ok, source_type = reaper.GetMediaSourceType(source, "")' not in result["script"]
    assert "project state" in result["summary"]


def test_generate_create_track_script_validates_name() -> None:
    result = generate_reascript("create_track", {"name": "04 GUITAR - Helix", "index": 3})

    assert result["action"] == "create_track"
    assert result["script_path"].endswith("create_track.lua")
    assert "reaper.InsertTrackAtIndex(3, true)" in result["script"]
    assert "P_NAME" in result["script"]
    assert "04 GUITAR - Helix" in result["script"]


def test_generate_create_track_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="name"):
        generate_reascript("create_track", {"name": ""})


def test_generate_unknown_action_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported"):
        generate_reascript("delete_everything", {})
