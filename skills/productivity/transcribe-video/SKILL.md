---
name: transcribe-video
description: Transcribes video or audio to plain text using Whisper. Use when the user wants to extract dialogue or speech from a local file or a URL (YouTube, Vimeo, or any yt-dlp-supported site), or says "transcribe this video", "transcribe this URL", "get the transcript", "extract the dialogue".
compatibility: Requires openai-whisper Python package, ffmpeg, and yt-dlp (for URL sources).
---

Extracts speech from a video or audio source and saves it as a `.txt` file.

## 1. Dependency check

Run these checks in parallel:

| Dependency | Check command | Required for |
|---|---|---|
| ffmpeg | `ffmpeg -version` | all sources |
| `openai-whisper` | `python -c "import whisper"` | all sources |
| yt-dlp | `yt-dlp --version` | URL sources only |

If any required dependency is missing, list all missing ones together and ask the user to confirm before installing. Install commands are in [references/install.md](references/install.md).

## 2. Model selection

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

## 3. Transcription

### From a URL

```bash
yt-dlp "<url>" -o "yt_tmp.%(ext)s" --no-playlist
```

Capture the downloaded filename from yt-dlp output, then:

```bash
whisper "<downloaded_file>" --model <model> --output_format txt
```

Delete the downloaded video file after transcription completes.

### From a local file

```bash
whisper "<file_path>" --model <model> --output_format txt
```

## 4. Output

Whisper writes `<source_name>.txt` in the working directory. Report the output path and offer to display the transcript inline.
