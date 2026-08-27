import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / 'extract_pdf.py'


def test_help() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), '--help'],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert 'Extract text from a PDF file.' in result.stdout


def test_missing_pdf_is_rejected(tmp_path: Path) -> None:
    missing_pdf = tmp_path / 'missing.pdf'
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(missing_pdf)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert 'PDF file not found' in result.stderr
