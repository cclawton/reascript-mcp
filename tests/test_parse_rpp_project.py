from pathlib import Path

import pytest

from reascript_mcp.tools.parse_rpp_project import parse_rpp_project


SIMPLE_RPP = """<REAPER_PROJECT 0.1 "7.0/macOS-arm64" 1750000000
  TEMPO 90 4 4
  <TRACK {11111111-1111-1111-1111-111111111111}
    NAME "Guitar DI"
    VOLPAN 1 0 -1 -1 1
    <ITEM
      POSITION 0
      LENGTH 4
      NAME "riff take"
      <SOURCE MIDI
        HASDATA 1 960 QN
      >
    >
  >
  <TRACK {22222222-2222-2222-2222-222222222222}
    NAME "Bass"
    <ITEM
      POSITION 4
      LENGTH 2
      NAME "bass answer"
      <SOURCE WAVE
        FILE "bass.wav"
      >
    >
  >
>"""


def test_parse_rpp_project_returns_project_summary(tmp_path: Path) -> None:
    project = tmp_path / "asian-sentry.rpp"
    project.write_text(SIMPLE_RPP)

    result = parse_rpp_project(str(project))

    assert result["project_path"] == str(project)
    assert result["tempo"]["bpm"] == 90.0
    assert result["time_signature"] == "4/4"
    assert result["track_count"] == 2
    assert result["item_count"] == 2
    assert result["tracks"][0] == {
        "index": 0,
        "name": "Guitar DI",
        "item_count": 1,
        "media_types": ["MIDI"],
    }
    assert result["tracks"][1]["media_types"] == ["WAVE"]
    assert "2 tracks" in result["summary"]


def test_parse_rpp_project_handles_unnamed_tracks(tmp_path: Path) -> None:
    project = tmp_path / "unnamed.rpp"
    project.write_text("""<REAPER_PROJECT 0.1 "7.0" 1
  <TRACK {11111111-1111-1111-1111-111111111111}
  >
>""")

    result = parse_rpp_project(str(project))

    assert result["tracks"][0]["name"] == "Track 1"
    assert result["tempo"] is None
    assert result["time_signature"] is None


def test_parse_rpp_project_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        parse_rpp_project(str(tmp_path / "missing.rpp"))


def test_parse_rpp_project_rejects_non_rpp(tmp_path: Path) -> None:
    project = tmp_path / "not-midi.txt"
    project.write_text(SIMPLE_RPP)

    with pytest.raises(ValueError, match=".rpp"):
        parse_rpp_project(str(project))
