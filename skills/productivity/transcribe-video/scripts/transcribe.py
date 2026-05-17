#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Transcription pipeline: URL or local file → yt-dlp (if URL) → whisper → cleanup.

Usage:
  uv run scripts/transcribe.py <source> --model <model> [--venv <venv-path>]

Arguments:
  source        URL (http/https) or path to a local audio/video file
  --model       Whisper model name: tiny, base, small, medium, large
  --venv        Path to the whisper venv directory (default: whisper-env)

Output:
  Prints the path of the generated transcript file on success.

Exit codes:
  0  success
  1  pipeline error
  2  usage error
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def venv_bin(venv: Path, name: str) -> str:
    win = venv / "Scripts" / name
    if win.with_suffix(".exe").exists() or win.exists():
        return str(win)
    return str(venv / "bin" / name)


def is_url(source: str) -> bool:
    return source.startswith("http://") or source.startswith("https://")


def download(source: str, yt_dlp: str) -> Path:
    result = subprocess.run(
        [yt_dlp, source, "-o", "yt_tmp.%(ext)s", "--no-playlist"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError("yt-dlp failed")

    match = re.search(r"\[download\] Destination: (.+)", result.stdout)
    if not match:
        match = re.search(r'\[Merger\] Merging formats into "(.+?)"', result.stdout)
    if not match:
        match = re.search(r"Destination: (.+)", result.stdout)
    if not match:
        raise RuntimeError("Could not determine downloaded filename from yt-dlp output")

    return Path(match.group(1).strip())


def transcribe(source_file: Path, whisper: str, model: str) -> Path:
    result = subprocess.run(
        [whisper, str(source_file), "--model", model, "--output_format", "txt"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError("whisper failed")

    transcript = Path(source_file.stem + ".txt")
    if not transcript.exists():
        raise RuntimeError(f"Expected transcript not found: {transcript}")
    return transcript


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe video or audio to text")
    parser.add_argument("source", help="URL or local file path")
    parser.add_argument("--model", required=True, help="Whisper model (tiny/base/small/medium/large)")
    parser.add_argument("--venv", default="whisper-env", help="Path to whisper venv (default: whisper-env)")

    args = parser.parse_args()
    venv = Path(args.venv)
    whisper = venv_bin(venv, "whisper")
    yt_dlp = venv_bin(venv, "yt-dlp")

    temp_file: Path | None = None
    try:
        if is_url(args.source):
            temp_file = download(args.source, yt_dlp)
            source_file = temp_file
        else:
            source_file = Path(args.source)
            if not source_file.exists():
                print(f"File not found: {source_file}", file=sys.stderr)
                return 2

        transcript = transcribe(source_file, whisper, args.model)
        print(str(transcript))
        return 0

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    finally:
        if temp_file and temp_file.exists():
            temp_file.unlink()


if __name__ == "__main__":
    sys.exit(main())
