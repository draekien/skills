---
name: transcribe-video
description: Transcribes video or audio to plain text using Whisper. Use when the user wants to extract dialogue or speech from a local file or a URL (YouTube, Vimeo, or any yt-dlp-supported site), or says "transcribe this video", "transcribe this URL", "get the transcript", "extract the dialogue".
compatibility: Requires uv and ffmpeg. openai-whisper, yt-dlp, and PyTorch are installed into an isolated venv during setup.
---

Extracts speech from a video or audio source and saves it as a `.txt` file.

## 1. Dependency check

Run these checks in parallel:

| Dependency | Check command |
|---|---|
| ffmpeg | `ffmpeg -version` |
| uv | `uv --version` |

If any dependency is missing, list all missing ones and ask the user to confirm before installing. Install commands are in [references/install.md](references/install.md).

## 2. Environment setup

Install Python 3.12 if not already available, then create an isolated venv and install dependencies:

```bash
uv python install 3.12
uv venv whisper-env --python 3.12
uv pip install --python whisper-env openai-whisper yt-dlp
```

### CUDA detection

Run `nvidia-smi` to check for an NVIDIA GPU. If no GPU is found, skip the rest of this section.

If an NVIDIA GPU is detected, install the PyTorch CUDA wheel:

```bash
uv pip install --python whisper-env torch --index-url https://download.pytorch.org/whl/cu124
```

Verify GPU is available:

- Windows: `whisper-env\Scripts\python -c "import torch; print(torch.cuda.is_available())"`
- Unix: `whisper-env/bin/python -c "import torch; print(torch.cuda.is_available())"`

If the result is `False`, warn the user: GPU acceleration is unavailable and CPU transcription with larger models may take 10–30× longer.

## 3. Model selection

Check memory for a saved `whisper-model` preference.

- **Found:** use it silently.
- **Not found:** present the table below, ask the user to choose, then save the choice to memory as a user preference keyed `whisper-model`.

| Model | Download size | Notes |
|---|---|---|
| tiny | ~75 MB | Fastest; clear audio only |
| base | ~150 MB | Good balance for most speech |
| small | ~500 MB | Better with accents or mild noise |
| medium | ~1.5 GB | Handles difficult audio |
| large | ~3 GB | Maximum accuracy |

## 4. Transcription

Use the venv-local binaries. Replace `<whisper>` and `<yt-dlp>` with:
- Windows: `whisper-env\Scripts\whisper` and `whisper-env\Scripts\yt-dlp`
- Unix: `whisper-env/bin/whisper` and `whisper-env/bin/yt-dlp`

### From a URL

```bash
<yt-dlp> "<url>" -o "yt_tmp.%(ext)s" --no-playlist
```

Capture the downloaded filename from yt-dlp output, then:

```bash
<whisper> "<downloaded_file>" --model <model> --output_format txt
```

Delete the downloaded video file after transcription completes.

### From a local file

```bash
<whisper> "<file_path>" --model <model> --output_format txt
```

## 5. Output

Whisper writes `<source_name>.txt` in the working directory. Report the output path and offer to display the transcript inline.
