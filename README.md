# PDF Text Extraction

[![CI](https://github.com/AbdullahFageeh/pdf-extraction-tool/actions/workflows/quality.yml/badge.svg)](https://github.com/AbdullahFageeh/pdf-extraction-tool/actions/workflows/quality.yml)

Small utility for extracting text from a PDF with PyPDF2.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
.\.venv\Scripts\python.exe extract_pdf.py path\to\file.pdf
```

The extracted text is written to the terminal. Redirect it to a file when needed:

```powershell
.\.venv\Scripts\python.exe extract_pdf.py path\to\file.pdf > output.txt
```

## Verify

```powershell
.\.venv\Scripts\python.exe -m py_compile extract_pdf.py
.\.venv\Scripts\python.exe extract_pdf.py --help
```

Keep source PDFs and generated output outside Git unless they are explicitly safe to share.
