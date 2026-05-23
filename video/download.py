import yt_dlp
import sys
import yaml
import subprocess
import json

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from transcribe import extract_md_file_name

def get_metadata_from_file(mp4_path: Path) -> dict:
    result = subprocess.run([
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        str(mp4_path)
    ], capture_output=True, text=True, encoding="utf-8")
    
    data = json.loads(result.stdout)
    tags = data.get("format", {}).get("tags", {})
    
    return {
        "title": tags.get("title"),
        "url": tags.get("comment") or tags.get("purl"),
        "channel": tags.get("artist") or tags.get("channel"),
        "upload_date": tags.get("date"),
        "duration": data.get("format", {}).get("duration"),
    }

def prepend_frontmatter(md_path: Path, metadata: dict):
    existing = md_path.read_text(encoding="utf-8")
    if existing.startswith("---"):
        print(f"Skipping {md_path.name} — frontmatter already exists")
        return
    frontmatter = yaml.dump(metadata, allow_unicode=True, sort_keys=False)
    md_path.write_text(f"---\n{frontmatter}---\n\n{existing}", encoding="utf-8")

# Extract the metadata from the .mp4 files we have and
# add them to the frontmatter of the .md transcript files.
def metadata_extract_and_load(vid) -> bool:
    md_path = extract_md_file_name(vid)
    if not md_path.exists():
        return False
    metadata = get_metadata_from_file(vid)  # or ffprobe fallback
    prepend_frontmatter(md_path, metadata)
    print(f"Updated {vid.stem}")
    return True

def main():
    vid_dir = Path(sys.argv[1]).glob("*.mp4")

    for video in vid_dir:
        metadata_extract_and_load(video)

if __name__ == '__main__':
    main()    