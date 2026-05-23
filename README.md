# Forager

A data ingestion pipeline that will expand as I need to add more resources to my personal corpus of knowledge.
Currently implements video transcription.

## Setup

```bash
uv sync
```

## Video RAG Processing

This repository serves as the pipeline for my video ingestion, transcription, and chunking for personal favorite podcasts and lectures.
Intended to be added to my [OpenRAG](https://github.com/linagora/openrag) knowledge.
Videos are great the first watch but referencing them later is a chore.

### What it does

Transcribes video files using Docling ASR pipeline with Whisper Turbo. Docling handles ffmpeg and Whisper local inference based on current hardware.

### Usage

```bash
uv run transcribe.py <file or directory> <extension>
```

Defaults to .mp4, see supported formats below.

### Supported formats

Docling's audio pipeline accepts: **WAV, MP3, M4A, AAC, OGG, FLAC**

It also accepts video files (**MP4, AVI, MOV**) — it extracts the audio track and transcribes it the same way.

# Development Plans

`yt-dlp` integration for the processing of videos not already on system.
