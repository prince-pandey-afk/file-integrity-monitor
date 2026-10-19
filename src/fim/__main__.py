
import argparse
import json
import sys
from pathlib import Path

from src.fim.monitor import create_baseline, scan_directory


def is_inside(path: Path, directory: Path) -> bool:
    """Check whether a path is inside a directory."""
    path = path.resolve()
    directory = directory.resolve()
    return path == directory or directory in path.parents


def main():
    parser = argparse.ArgumentParser(
        description="File Integrity Monitor - detect file changes using SHA-256."
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True,
    )

    for command, help_text in [
        ("init", "Create a trusted file baseline"),
        ("scan", "Compare files against a saved baseline"),
    ]:
        subparser = commands.add_parser(command, help=help_text)
        subparser.add_argument(
            "directory",
            type=Path,
            help="Directory to monitor",
        )
        subparser.add_argument(
            "--baseline",
            type=Path,
            default=Path(".fim-baseline.json"),
            help="Baseline JSON path (default: .fim-baseline.json)",
        )

    args = parser.parse_args()
    directory = args.directory.resolve()
    baseline_path = args.baseline.resolve()

    if not directory.is_dir():
        parser.error(f"Directory does not exist: {directory}")

    if is_inside(baseline_path, directory):
        parser.error("Store the baseline outside the monitored directory.")

    if args.command == "init":
        try:
            baseline = create_baseline(directory)
            baseline_path.parent.mkdir(parents=True, exist_ok=True)

            with baseline_path.open("w", encoding="utf-8") as file:
                json.dump(baseline, file, indent=2)

        except OSError as error:
            parser.error(f"Could not create baseline: {error}")

        print(f"Baseline saved: {baseline_path}")
        print(f"Files recorded: {len(baseline)}")
        return

    if not baseline_path.is_file():
        parser.error(
            f"Baseline not found: {baseline_path}. Run init first."
        )

    try:
        with baseline_path.open("r", encoding="utf-8") as file:
            baseline = json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        parser.error(f"Could not load baseline: {error}")

    if not isinstance(baseline, dict) or not all(
        isinstance(path, str)
        and isinstance(file_hash, str)
        and len(file_hash) == 64
        and all(char in "0123456789abcdef" for char in file_hash)
        for path, file_hash in baseline.items()
    ):
        parser.error("Baseline is invalid or has an unsupported format.")

    try:
        results = scan_directory(directory, baseline)
    except OSError as error:
        parser.error(f"Could not scan files: {error}")

    for change_type, paths in results.items():
        print(f"{change_type.title()}: {len(paths)}")
        for path in paths:
            print(f"  - {path}")

    if any(results.values()):
        print("\nWARNING: File changes detected!")
        sys.exit(1)

    print("\nNo changes detected.")


if __name__ == "__main__":
    main()
