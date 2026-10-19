# File Integrity Monitor (FIM)

A Python cybersecurity project that detects unauthorized file changes using SHA-256 cryptographic hashes.

## Features

- Calculate SHA-256 hashes for files.
- Create and save file integrity baselines in JSON format.
- Detect modified, added, and deleted files.
- Scan directories recursively.
- Provide a command-line interface.
- Return a nonzero exit code when changes are detected.
- Validate baseline format before scanning.
- Include automated tests with pytest.

## Requirements

- Python 3.10 or newer
- Git
- pytest for development and testing

## Setup

Clone the repository, then enter the project directory:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd file-integrity-monitor
```

Create and activate a virtual environment on Linux or WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the development test dependency:

```bash
python -m pip install pytest
```

## Usage

Create a directory to monitor:

```bash
mkdir -p important-files
echo "Original configuration" > important-files/config.txt
```

Create a baseline:

```bash
python -m src.fim init important-files
```

Scan for changes:

```bash
python -m src.fim scan important-files
```

Use a custom baseline location:

```bash
python -m src.fim init important-files --baseline baselines/config.json
python -m src.fim scan important-files --baseline baselines/config.json
```

If a file changes, the scanner reports the change and exits with status code `1`. A clean scan exits with status code `0`.

## How It Works

1. The program reads files in binary mode.
2. SHA-256 generates a digest for each file.
3. The baseline stores relative file paths and their digests.
4. A later scan calculates current digests and compares them with the saved baseline.
5. Differences identify modified, added, or deleted files.

## Security Considerations

- SHA-256 detects content changes but does not encrypt files.
- A baseline is only trustworthy if its integrity is protected.
- An attacker who can change both monitored files and the baseline may hide tampering.
- Store baselines outside the monitored directory.
- This is an educational defensive-security project, not a replacement for enterprise monitoring software.

## Project Structure

```text
src/
  fim/
    __init__.py
    __main__.py
    monitor.py
tests/
  test_monitor.py
.gitignore
README.md
requirements.txt
```

## Testing

Run the automated tests:

```bash
python -m pytest -v
```

## Learning Goals

This project demonstrates Python file handling, cryptographic hashing, JSON serialization, command-line argument parsing, Git version control, and automated testing.

## License

MIT License (add a LICENSE file before distributing the project under this license).
