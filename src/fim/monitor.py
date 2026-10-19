import hashlib
import json
from pathlib import Path


def calculate_hash(file_path: Path) -> str:
    """Calculate the SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def create_baseline(directory: Path) -> dict[str, str]:
    """Create a baseline of file paths and their SHA-256 hashes."""

    baseline = {}

    for file_path in directory.rglob("*"):
        if file_path.is_file():
            relative_path = str(file_path.relative_to(directory))
            baseline[relative_path] = calculate_hash(file_path)

    return baseline


def save_baseline(baseline: dict[str, str], output_path: Path) -> None:
    """Save the baseline as a JSON file."""

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(baseline, file, indent=4)


def load_baseline(input_path: Path) -> dict[str, str]:
    """Load a saved baseline from a JSON file."""

    with input_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def scan_directory(
    directory: Path,
    baseline: dict[str, str],
) -> dict[str, list[str]]:
    """Compare current files against a saved baseline."""

    current_files = create_baseline(directory)

    baseline_paths = set(baseline)
    current_paths = set(current_files)

    modified = [
        path for path in baseline_paths & current_paths
        if baseline[path] != current_files[path]
    ]

    deleted = sorted(baseline_paths - current_paths)
    added = sorted(current_paths - baseline_paths)

    return {
        "modified": sorted(modified),
        "deleted": deleted,
        "added": added,
    }

