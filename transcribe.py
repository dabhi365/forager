from pathlib import Path
import json
import sys
import re

from docling.datamodel import asr_model_specs
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import AsrPipelineOptions
from docling.document_converter import AudioFormatOption, DocumentConverter
from docling.pipeline.asr_pipeline import AsrPipeline
from docling_core.types.doc.document import DoclingDocument



OUTPUT = Path("data")

class TranscriptResult:
    def __init__(self, document: DoclingDocument, path: Path):
        self.document = document
        # self.markdown = markdown
        self.path     = path

def transcribe_audio (
        file_path: Path
) -> TranscriptResult:    
    # Validation and Resolution of Path handled by main()
    # file_path = file_path.resolve()
    # if not file_path.exists():
    #     raise FileNotFoundError

    pipeline_options = AsrPipelineOptions()
    pipeline_options.asr_options = asr_model_specs.WHISPER_TURBO.model_copy(update={
                                                                                    "verbose": False,
                                                                                    "language": "en",
                                                                                    })

    converter = DocumentConverter(
        format_options={
            InputFormat.AUDIO: AudioFormatOption(
                pipeline_cls=AsrPipeline,
                pipeline_options=pipeline_options,
            )
        }
    )

    result = converter.convert(file_path)
    doc = result.document

    return TranscriptResult(
        document=doc,
        path = file_path
    )

def extract_md_file_name(path: Path) -> Path:
    try:
        match = re.search(r'\[([^\[\]]+)\]$', path.stem)
        name = match.group(1) if match else path.stem
    except Exception as e:
        print(f"Warning: couldn't parse {path.name}: {e}")
        name = path.stem
    return OUTPUT / f"{name}.md"
    
def format_timestamp(seconds: float) -> str:
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"[{h:02d}:{m:02d}:{s:02d}]"

def export_markdown_with_timestamps(result: TranscriptResult):
    file_name = extract_md_file_name(result.path)

    write_lines = []

    for item in result.document.texts:
        text = item.text.strip()
        if not text:
            continue

        start_time = None
        if item.source:
            first_source = item.source[0]
            start_time = getattr(first_source, 'start_time', None)

        if start_time is not None:
            write_lines.append(f"`{format_timestamp(start_time)}` {text}")
        else:
            write_lines.append(text)

    file_name.write_text("\n\n".join(write_lines), encoding="utf-8")

def main():
    directory = False
    file   = False
    
    ext = "mp4"
    accepted_ext = ('wav, mp3, m4a, aac, ogg, flac, mp4, avi, mov')

    resolved_path = Path()

    # parse arguments
    arg_path = sys.argv[1]
    if len(sys.argv) > 2:
        if sys.argv[2] in accepted_ext:
            ext = sys.argv[2]
        else:
            raise ValueError(f"Extension not: {accepted_ext}")

    # establish Path and resolve
    if Path(arg_path).is_dir():
        directory = True
        resolved_path = Path(arg_path).resolve()
    else:
        file = True
        resolved_path = Path(arg_path).resolve()

    if directory:
        video_list = list(resolved_path.glob(f"*.{ext}"))
        print(f"Found directory of .{ext} files.\nContains {len(video_list)} .{ext} files.")

        for video in video_list:
            if (OUTPUT / extract_md_file_name(video)).exists():
                print(f"Skipping {video}, Already processed")
            result = transcribe_audio(video)
            export_markdown_with_timestamps(result)


if __name__ == "__main__":
    main()
