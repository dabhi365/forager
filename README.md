# Video RAG Processing

This repository serves as the pipeline for my video ingestion, transcription, and chunking for personal favorite podcasts and lectures.
Intended to be added to my [OpenRAG](https://github.com/linagora/openrag) knowledge.
Videos are great the first watch but referencing them later is a chore.

## What it does

Transcribes video files using Docling ASR pipeline with Whisper Turbo. Docling handles ffmpeg and Whisper local inference based on current hardware.

## Setup

```bash
uv sync
```

## Usage

```bash
uv run python transcribe.py <file or directory> <extension>
```

Defaults to .mp4, see supported formats below.

## Supported formats

Docling's audio pipeline accepts: **WAV, MP3, M4A, AAC, OGG, FLAC**

It also accepts video files (**MP4, AVI, MOV**) — it extracts the audio track and transcribes it the same way.

## Limitations

- **No SRT/VTT output.** Docling exports to Markdown, HTML, DocTags, and JSON. It does not produce subtitle formats like SRT or WebVTT with per-line timestamps. If you need SRT, use `openai-whisper` directly (`whisper audio.mp3 --output_format srt`).
- **Transcript only, no speaker diarization.** You get a flat transcript without speaker labels.
- **Paragraph-level text.** The output is sentence/paragraph-level Markdown, not word-level or segment-level with timestamps.
