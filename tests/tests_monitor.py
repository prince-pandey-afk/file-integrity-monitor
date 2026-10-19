from pathlib import Path

from src.fim.monitor import (
    calculate_hash,
    create_baseline,
    scan_directory,
)


def test_same_file_has_same_hash(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("hello world", encoding="utf-8")

    assert calculate_hash(file_path) == calculate_hash(file_path)


def test_changed_file_is_detected(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("original", encoding="utf-8")

    baseline = create_baseline(tmp_path)

    file_path.write_text("modified", encoding="utf-8")

    results = scan_directory(tmp_path, baseline)

    assert results["modified"] == ["example.txt"]


def test_new_file_is_detected(tmp_path):
    baseline_dir = tmp_path / "baseline"
    baseline_dir.mkdir()

    baseline = create_baseline(baseline_dir)

    (baseline_dir / "new.txt").write_text("new file", encoding="utf-8")

    results = scan_directory(baseline_dir, baseline)

    assert results["added"] == ["new.txt"]


def test_deleted_file_is_detected(tmp_path):
    file_path = tmp_path / "delete_me.txt"
    file_path.write_text("important", encoding="utf-8")

    baseline = create_baseline(tmp_path)

    file_path.unlink()

    results = scan_directory(tmp_path, baseline)

    assert results["deleted"] == ["delete_me.txt"]