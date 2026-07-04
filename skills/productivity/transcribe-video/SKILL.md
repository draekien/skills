---
name: transcribe-video
description: Transcribes video or audio to plain text. Use when you have a local file or a URL, such as YouTube or Vimeo, and want the spoken dialogue extracted as text.
compatibility: Requires uv and ffmpeg. openai-whisper, yt-dlp, and PyTorch are installed into an isolated venv during setup.
disable-model-invocation: true
---

Extracts speech from a video or audio source and saves it as a `.txt` file.

## Available scripts

- **`scripts/transcribe.py`** — Downloads (if URL), transcribes with Whisper, and writes a `.txt` file.

## 1. Dependency check

Run these checks in parallel:

| Dependency | Check command |
|---|---|
| ffmpeg | `ffmpeg -version` |
| uv | `uv --version` |

If ffmpeg or uv is missing, list all missing system tools and ask the user to confirm before running the install commands. No confirmation is needed for Python packages installed into the venv. Install commands are in [references/install.md](references/install.md).

## 2. Environment setup

Check whether the environment is already set up:

- Windows: `whisper-env\Scripts\pip show openai-whisper yt-dlp`
- Unix: `whisper-env/bin/pip show openai-whisper yt-dlp`

If both packages are found, skip to the **CUDA check** step below.

Otherwise, install Python 3.12 and create the venv:

```bash
uv python install 3.12
uv venv whisper-env --python 3.12
```

Run `nvidia-smi` to detect an NVIDIA GPU.

**NVIDIA GPU detected** — install PyTorch from the CUDA wheel index first, then install the remaining dependencies. Installing torch before openai-whisper ensures its torch dependency resolves to the CUDA build rather than the CPU build from PyPI:

```bash
uv pip install --python whisper-env torch --index-url https://download.pytorch.org/whl/cu124
uv pip install --python whisper-env openai-whisper yt-dlp
```

**No GPU found** — install dependencies directly (openai-whisper will pull in the CPU torch build):

```bash
uv pip install --python whisper-env openai-whisper yt-dlp
```

**CUDA check** — run this whether or not the env was already set up:

- Windows: `whisper-env\Scripts\python -c "import torch; print(torch.cuda.is_available())"`
- Unix: `whisper-env/bin/python -c "import torch; print(torch.cuda.is_available())"`

If the result is `False`, warn the user: GPU acceleration is unavailable and CPU transcription with larger models may take 10–30× longer.

## 3. Model selection

Check memory for a saved `whisper-model` preference.

- **Found:** use it, but tell the user which model is being used and offer to change it.
- **Not found:** present the table below, ask the user to choose, then save the choice to memory as a user preference keyed `whisper-model`.

| Model | Download size | Notes |
|---|---|---|
| tiny | ~75 MB | Fastest; clear audio only |
| base | ~150 MB | Good balance for most speech |
| small | ~500 MB | Better with accents or mild noise |
| medium | ~1.5 GB | Handles difficult audio |
| large | ~3 GB | Maximum accuracy |

## 4. Transcription

Run from the repo root (the directory containing `whisper-env`):

```bash
uv run scripts/transcribe.py "<source>" --model <model> --venv whisper-env
```

`<source>` is the URL or local file path. The script handles download (for URLs), transcription, and temp file cleanup automatically. It prints the transcript file path on success.

If the script exits non-zero, read its stderr and report it verbatim. Common causes: unsupported URL, private/geo-blocked video, corrupted local file.

## 5. Output

The script prints the exact output path on success. Report that path; do not infer the filename yourself. Offer to display the transcript inline.
