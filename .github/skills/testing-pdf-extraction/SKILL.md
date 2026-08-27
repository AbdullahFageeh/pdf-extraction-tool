---
name: testing-pdf-extraction
description: "Run, write, and debug tests for the PDF extraction tool. Use when: adding new tests, debugging test failures, creating PDF fixtures with reportlab, or running the test suite. Covers pytest setup, PDF fixture generation, and test patterns."
---

# Testing PDF Extraction

## Run Tests

```powershell
.\.venv\Scripts\pytest.exe -v
```

## Test Structure

- `tests/test_pdf_extraction.py` — Integration tests (PDF generation + extraction)
- `tests/test_extract_pdf.py` — CLI behavior tests (help flag, error exits)

## PDF Fixture Helpers

Use **reportlab** to create test PDFs in-memory:

```python
from io import BytesIO
from reportlab.pdfgen import canvas

def _create_pdf(text_lines):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    for line in text_lines:
        c.drawString(100, 750, line)
        c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
```

## Test Patterns

| Test Type | Pattern |
|---|---|
| Basic extraction | Create PDF → extract → assert text content |
| Multi-page | Create multi-page PDF → check page separators |
| Missing file | `subprocess.run(['extract-pdf', 'nonexistent.pdf'])` → check returncode |
| Help flag | `extract-pdf --help` → check output contains usage |
| Invalid backend | `--backend invalid` → check returncode != 0 |
| Non-PDF file | Write text file → extract → check error exit |

## Key Dependencies

- `pytest` — test runner
- `reportlab` — PDF fixture generation
- `subprocess` — CLI invocation testing

## CI Testing

Tests run in `.github/workflows/quality.yml`:
```yaml
- run: pytest
```

Run with `--tb=short` in CI for concise output.