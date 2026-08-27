import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent / 'fixtures'
SCRIPT = Path(__file__).parents[1] / 'extract_pdf.py'
SAMPLE_PDF = FIXTURES / 'sample.pdf'


def test_extracts_text_from_sample_pdf() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(SAMPLE_PDF)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert 'Number of pages: 1' in result.stdout
    assert 'Hello, World!' in result.stdout


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
