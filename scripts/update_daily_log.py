import argparse
import datetime
import os
import random
import uuid

DEFAULT_NOTES = [
    "hello my guys",
    "the green squares are real",
    "there is no antimemetics division",
    "Seneca sucks",
    "daily beep boop",
    "commit added for the vibes and the optics",
    "not a masterpiece",
]


def append_log(output_dir: str, date_str: str | None, seed: int | None, note: str | None) -> str:
    if seed is not None:
        random.seed(seed)

    if date_str is None:
        date_str = datetime.date.today().isoformat()

    timestamp = datetime.datetime.now().strftime("%H:%M")
    message = note or random.choice(DEFAULT_NOTES)
    token = uuid.uuid4().hex[:6]

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{date_str}.md")
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(f"- {timestamp} {message} ({token})\n")

    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Append a small daily log entry.")
    parser.add_argument("--output-dir", default="logs", help="Directory for daily log files.")
    parser.add_argument("--date", dest="date_str", default=None, help="Override date (YYYY-MM-DD).")
    parser.add_argument("--seed", type=int, default=None, help="Seed for deterministic note selection.")
    parser.add_argument("--note", default=None, help="Explicit note text (overrides random selection).")
    args = parser.parse_args()

    append_log(args.output_dir, args.date_str, args.seed, args.note)


if __name__ == "__main__":
    main()
