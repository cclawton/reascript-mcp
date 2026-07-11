"""Parse Reaper .rpp project files into a compact JSON-friendly summary."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any


_TRACK_START_RE = re.compile(r"^\s*<TRACK\b")
_ITEM_START_RE = re.compile(r"^\s*<ITEM\b")
_SOURCE_RE = re.compile(r"^\s*<SOURCE\s+(\S+)")
_NAME_RE = re.compile(r'^\s*NAME\s+"(.*)"')
_TEMPO_RE = re.compile(r"^\s*TEMPO\s+([0-9.]+)\s+(\d+)\s+(\d+)")
_VST_RE = re.compile(r'^\s*<VST\s+"(.+?)"\s+("[^"]+"|\S+)')
_PRESETNAME_RE = re.compile(r'^\s*PRESETNAME\s+"?(.*?)"?\s*$')


def parse_rpp_project(project_path: str) -> dict[str, Any]:
    """Return a compact summary of a Reaper project file.

    The parser intentionally handles the subset needed for LLM state readback:
    project timing, track names, item counts, and media source types. It does not
    mutate the project and can run without Reaper installed.
    """

    path = Path(project_path).expanduser()
    if path.suffix.lower() != ".rpp":
        raise ValueError("project_path must point to a .rpp Reaper project file")
    if not path.exists():
        raise FileNotFoundError(f"Reaper project not found: {path}")

    text = path.read_text(errors="replace")
    lines = text.splitlines()

    tempo: dict[str, Any] | None = None
    time_signature: str | None = None
    tracks: list[dict[str, Any]] = []
    current_track: dict[str, Any] | None = None
    current_item_media_types: list[str] = []
    inside_item = False
    inside_fxchain = False
    fx_depth = 0

    for line in lines:
        if tempo is None:
            tempo_match = _TEMPO_RE.match(line)
            if tempo_match:
                bpm, numerator, denominator = tempo_match.groups()
                tempo = {"bpm": float(bpm)}
                time_signature = f"{numerator}/{denominator}"

        if _TRACK_START_RE.match(line):
            current_track = {
                "index": len(tracks),
                "name": f"Track {len(tracks) + 1}",
                "item_count": 0,
                "media_types": [],
                "fx": [],
            }
            tracks.append(current_track)
            inside_item = False
            inside_fxchain = False
            fx_depth = 0
            current_item_media_types = []
            continue

        if current_track is None:
            continue

        name_match = _NAME_RE.match(line)
        if name_match and not inside_item:
            current_track["name"] = name_match.group(1)
            continue

        if _ITEM_START_RE.match(line):
            inside_item = True
            current_track["item_count"] += 1
            current_item_media_types = []
            continue

        if inside_item:
            source_match = _SOURCE_RE.match(line)
            if source_match:
                media_type = source_match.group(1).upper()
                if media_type not in current_item_media_types:
                    current_item_media_types.append(media_type)
                if media_type not in current_track["media_types"]:
                    current_track["media_types"].append(media_type)

            if line.strip() == ">":
                inside_item = False
                current_item_media_types = []
            continue

        if "<FXCHAIN" in line:
            inside_fxchain = True
            fx_depth = 1
            continue

        if inside_fxchain:
            vst_match = _VST_RE.match(line)
            if vst_match:
                fx_name, fx_file_raw = vst_match.groups()
                fx_file = fx_file_raw.strip('"')
                current_track["fx"].append({
                    "name": fx_name,
                    "file": fx_file,
                    "preset": None,
                })
                fx_depth += 1
                continue

            preset_match = _PRESETNAME_RE.match(line)
            if preset_match and current_track["fx"]:
                current_track["fx"][-1]["preset"] = preset_match.group(1)
                continue

            if line.strip() == ">":
                fx_depth -= 1
                if fx_depth <= 0:
                    inside_fxchain = False
                continue

            if line.strip().startswith("<") and "<FXCHAIN" not in line:
                fx_depth += 1

    item_count = sum(track["item_count"] for track in tracks)
    summary = f"{path.name}: {len(tracks)} tracks, {item_count} media items"
    if tempo and time_signature:
        summary += f", {tempo['bpm']:g} BPM, {time_signature}"

    return {
        "project_path": str(path),
        "tempo": tempo,
        "time_signature": time_signature,
        "track_count": len(tracks),
        "item_count": item_count,
        "tracks": tracks,
        "summary": summary,
    }
