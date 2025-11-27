from __future__ import annotations

import argparse
import base64
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

@dataclass
class ImageRecord:
    job_id: str
    filename: str
    mime: str
    base64_data: str

    @classmethod
    def from_json_payload(cls, payload: Dict[str, Any]) -> "ImageRecord":
        annotated = payload["annotated_image"]

        return cls(
            job_id=payload.get("job_id", "unknown_job"),
            filename=annotated.get("filename", "image"),
            mime=annotated.get("mime", "application/octet-stream"),
            base64_data=annotated["base64"],
        )

    def guess_extension(self) -> str:
        mime = (self.mime or "").lower()

        mime_to_ext = {
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/png":  ".png",
            "image/webp": ".webp",
        }

        if mime in mime_to_ext:
            return mime_to_ext[mime]

        original_suffix = Path(self.filename).suffix
        return original_suffix or ".bin"

    def build_output_path(self, output_dir: Path) -> Path:
        output_dir = output_dir.expanduser().resolve()
        stem = Path(self.filename).stem or self.job_id
        ext = self.guess_extension()
        return output_dir / f"{stem}{ext}"

    def decode_to_file(self, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)

        out_path = self.build_output_path(output_dir)
        binary_data = base64.b64decode(self.base64_data)

        out_path.write_bytes(binary_data)
        return out_path

def convert_single_json(json_path: Path, output_dir: Path) -> Path | None:
    try:
        with json_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[ERROR] Failed to read/parse {json_path.name}: {exc}")
        return None

    try:
        record = ImageRecord.from_json_payload(payload)
    except KeyError as exc:
        print(f"[WARN] {json_path.name}: missing key {exc}, skipping.")
        return None

    try:
        out_path = record.decode_to_file(output_dir)
    except (OSError, ValueError, base64.binascii.Error) as exc:
        print(f"[ERROR] Failed to decode image from {json_path.name}: {exc}")
        return None

    print(f"[OK] {json_path.name}  ->  {out_path.name}")
    return out_path


def convert_folder(input_dir: Path, output_dir: Path) -> None:
    input_dir = input_dir.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()

    json_files = sorted(input_dir.glob("*.json"))

    if not json_files:
        print(f"[INFO] No .json files found in {input_dir}")
        return

    print(f"[INFO] Found {len(json_files)} JSON file(s) in {input_dir}")
    print(f"[INFO] Output images will be written to {output_dir}")
    print("-" * 60)

    for json_path in json_files:
        convert_single_json(json_path, output_dir)

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Decode base64 images from JSON files into image files."
    )
    parser.add_argument(
        "input_dir",
        help="Folder containing JSON files with base64 images.",
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="decoded_images",
        help="Folder where decoded images will be stored (default: decoded_images).",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    convert_folder(input_dir, output_dir)


if __name__ == "__main__":
    main()
