# PDF Text Extraction

[![CI](https://github.com/AbdullahFageeh/pdf-extraction-tool/actions/workflows/quality.yml/badge.svg)](https://github.com/AbdullahFageeh/pdf-extraction-tool/actions/workflows/quality.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Small utility for extracting text from PDF files with multiple backend support.

## Installation

```powershell
pip install pdf-extraction-tool
```

Or from source:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,backends]"
```

## Usage

```powershell
# Basic usage (uses PyPDF2 backend)
extract-pdf path\to\file.pdf

# Use pdfminer backend (requires pdfminer.six)
extract-pdf --backend pdfminer path\to\file.pdf

# Extract from encrypted PDF
extract-pdf --password secret path\to\file.pdf
```

The extracted text is written to the terminal. Redirect it to a file when needed:

```powershell
extract-pdf path\to\file.pdf > output.txt
```

## Backends

| Backend            | Install                    | Notes                                             |
| ------------------ | -------------------------- | ------------------------------------------------- |
| `pypdf2` (default) | Included                   | Fast, good for most PDFs                          |
| `pdfminer`         | `pip install pdfminer.six` | Better layout preservation, handles complex fonts |

## Verify

```powershell
python -m py_compile extract_pdf.py
extract-pdf --help
```

Keep source PDFs and generated output outside Git unless they are explicitly safe to share.
