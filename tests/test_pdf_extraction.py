import subprocess
import sys
from pathlib import Path

import pytest

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None  # type: ignore[assignment]

FIXTURES = Path(__file__).parent / 'fixtures'
SCRIPT = Path(__file__).parents[1] / 'extract_pdf.py'
SAMPLE_PDF = FIXTURES / 'sample.pdf'


def _create_multiline_pdf(path: Path) -> Path:
    """Create a PDF with 'Hello, World!' text."""
    if PyPDF2 is None:
        pytest.skip('PyPDF2 not installed')
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(str(path), pagesize=letter)
    c.drawString(100, 700, 'Hello, World!')
    c.save()
    return path


def _create_multipage_pdf(path: Path, num_pages: int = 3) -> Path:
    """Create a PDF with multiple pages of text."""
    if PyPDF2 is None:
        pytest.skip('PyPDF2 not installed')
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(str(path), pagesize=letter)
    for i in range(num_pages):
        c.drawString(100, 700, f'Page {i + 1} content')
        c.showPage()
    c.save()
    return path


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


def test_extracts_multiple_pages(tmp_path: Path) -> None:
    pdf = tmp_path / 'multipage.pdf'
    _create_multipage_pdf(pdf, num_pages=3)

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(pdf)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert 'Number of pages: 3' in result.stdout
    assert 'Page 1 content' in result.stdout
    assert 'Page 2 content' in result.stdout
    assert 'Page 3 content' in result.stdout


def test_help_flag() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), '--help'],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert 'Extract text from a PDF file' in result.stdout
    assert '--backend' in result.stdout
    assert '--password' in result.stdout


def test_backend_option_exists() -> None:
    """Test that --backend flag is recognized (pypdf2 should work without extra install)."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), '--backend', 'pypdf2', str(SAMPLE_PDF)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert 'Hello, World!' in result.stdout


def test_invalid_backend_rejected() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), '--backend', 'invalid', str(SAMPLE_PDF)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert 'invalid' in result.stderr.lower() or 'choice' in result.stderr.lower()


def test_non_pdf_file_handled(tmp_path: Path) -> None:
    """Test that non-PDF files produce a meaningful error."""
    not_pdf = tmp_path / 'not_a_pdf.txt'
    not_pdf.write_text('This is not a PDF file')

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(not_pdf)],
        capture_output=True,
        text=True,
        check=False,
    )

    # Should fail gracefully (non-zero exit code) with an error message
    assert result.returncode != 0
    assert 'error' in result.stderr.lower() or result.stderr.strip()
