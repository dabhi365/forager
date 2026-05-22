from pathlib import Path
import json
import sys

from docling.datamodel import asr_model_specs
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import AsrPipelineOptions
from docling.document_converter import AudioFormatOption, DocumentConverter
from docling.pipeline.asr_pipeline import AsrPipeline



OUTPUT = Path("data").resolve()

class TranscriptResult:
    def __init__(self, document, markdown):
        self.document = document
        self.markdown = markdown

def transcribe_audio (
        audio_path: Path
) -> TranscriptResult:    
    audio_path = audio_path.resolve()
    if not audio_path.exists():
        raise FileNotFoundError

    pipeline_options = AsrPipelineOptions()
    pipeline_options.asr_options = asr_model_specs.WHISPER_TURBO

    converter = DocumentConverter(
        format_options={
            InputFormat.AUDIO: AudioFormatOption(
                pipeline_cls=AsrPipeline,
                pipeline_options=pipeline_options,
            )
        }
    )

    result = converter.convert(audio_path)
    doc = result.document

    # Save markdown transcript
    md = doc.export_to_markdown()
    
    with open("transcript.json", "w") as f:
        json.dump(doc.export_to_dict(), f, indent=4)

    return TranscriptResult(
        document=doc,
        markdown=md
    )

def main():
    # result = transcribe_audio(Path("E:\\Videos\\WRO\\001 - WRO #9 21-Day EMA Part 1, Webby Rambles On (Slight Return) [GxQpyUfZv4U].mp4"))
    
    directory = False
    file   = False
    ext = "mp4"
    resolved_path = Path()

    # parse arguments
    arg_path = sys.argv[1]
    if sys.argv[2]:
        ext = sys.argv[2]

    # establish Path and resolve
    if Path(arg_path).is_dir():
        directory = True
        resolved_path = Path(arg_path).resolve()
    else:
        file = True
        resolved_path = Path(arg_path).resolve()

    if directory:
        transcription_list = resolved_path.glob(f"*.{ext}")
        print(transcription_list)

if __name__ == "__main__":
    main()
