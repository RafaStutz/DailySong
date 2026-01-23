import argparse
import datetime
import json
import math
import os
import re
import shutil
from styles import JazzPianoStyle, JazzConfig

DEFAULT_DURATION_S = 90
MIN_DURATION_S = 60
MAX_DURATION_S = 120
BEATS_PER_MEASURE = 4


def clamp_duration(duration_s: int | None) -> int:
    if duration_s is None:
        duration_s = DEFAULT_DURATION_S
    return max(MIN_DURATION_S, min(MAX_DURATION_S, duration_s))


def measures_for_duration(duration_s: int, bpm: int) -> int:
    return math.ceil((duration_s * bpm) / (60 * BEATS_PER_MEASURE))


def prune_songs(output_dir: str, keep_last: int = 3) -> None:
    pattern = re.compile(r"song_(\d{4}-\d{2}-\d{2})_.*\.(mid|mp3)$")
    songs = []
    dates = set()

    for name in os.listdir(output_dir):
        match = pattern.match(name)
        if not match:
            continue
        date_str = match.group(1)
        dates.add(date_str)
        songs.append((date_str, os.path.join(output_dir, name)))

    if not dates:
        return

    keep_dates = set(sorted(dates)[-keep_last:])
    for date_str, path in songs:
        if date_str not in keep_dates:
            os.remove(path)


def main(output_dir: str = "music", date_override: str | None = None, keep_last: int = 3) -> str:
    try:
        with open("state.json") as f:
            state = json.load(f)
    except FileNotFoundError:
        state = {"min_duration_s": DEFAULT_DURATION_S}

    config = JazzConfig()
    style = JazzPianoStyle(config)

    duration_s = clamp_duration(state.get("min_duration_s"))
    measures = measures_for_duration(duration_s, style.bpm)
    mid = style.next_song(measures)

    if date_override:
        date_str = date_override
    else:
        date_str = datetime.date.today().isoformat()

    filename = f"song_{date_str}_{style.bpm}bpm.mid"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    mid.save(output_path)
    latest_path = os.path.join(output_dir, "latest.mid")
    shutil.copyfile(output_path, latest_path)
    prune_songs(output_dir, keep_last=keep_last)
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a daily jazz MIDI file.")
    parser.add_argument("--output-dir", default="music", help="Directory to write MIDI files.")
    parser.add_argument("--date", dest="date_override", default=None, help="Override date (YYYY-MM-DD).")
    parser.add_argument("--keep-last", type=int, default=3, help="Keep only the last N song dates.")
    args = parser.parse_args()
    main(output_dir=args.output_dir, date_override=args.date_override, keep_last=args.keep_last)
