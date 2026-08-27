import argparse
import sys
from pathlib import Path

import PyPDF2


def extract_text_pypdf2(pdf_path: Path, password: str | None = None) -> str:
    """Extract text using PyPDF2."""
    reader = PyPDF2.PdfReader(pdf_path)
    if reader.is_encrypted:
        if not password:
            msg = 'Error: PDF is encrypted. Use --password to provide a password.'
            print(msg, file=sys.stderr)
            sys.exit(1)
        try:
            reader.decrypt(password)
        except PyPDF2.errors.PdfReadError as e:
            print(f'Error: Failed to decrypt PDF: {e}', file=sys.stderr)
            sys.exit(1)

    pages_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ''
        pages_text.append(f'--- Page {i + 1} ---\n{text}')

    separator = '=' * 80
    header = f'Number of pages: {len(reader.pages)}\n{separator}'
    body = '\n'.join(pages_text)
    return f'{header}\n{body}\n{separator}'


def extract_text_pdfminer(pdf_path: Path, password: str | None = None) -> str:
    """Extract text using pdfminer.six (optional backend)."""
    try:
        from pdfminer.high_level import extract_text as _extract  # type: ignore[import-not-found]
    except ImportError:
        msg = 'Error: pdfminer.six is not installed. Install with: pip install pdfminer.six'
        print(msg, file=sys.stderr)
        sys.exit(1)

    return _extract(pdf_path, password=password)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Extract text from a PDF file.',
        epilog='Backends: pypdf2 (default), pdfminer (requires pdfminer.six)',
    )
    parser.add_argument('pdf_path', type=Path, help='path to the PDF file')
    parser.add_argument(
        '--backend',
        choices=['pypdf2', 'pdfminer'],
        default='pypdf2',
        help='text extraction backend (default: pypdf2)',
    )
    parser.add_argument('--password', default=None, help='password for encrypted PDFs')
    args = parser.parse_args()

    if not args.pdf_path.is_file():
        parser.error(f'PDF file not found: {args.pdf_path}')

    try:
        if args.backend == 'pypdf2':
            text = extract_text_pypdf2(args.pdf_path, args.password)
        else:
            text = extract_text_pdfminer(args.pdf_path, args.password)
    except PyPDF2.errors.PdfReadError as e:
        print(f'Error: Failed to read PDF: {e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

    print(text)


if __name__ == '__main__':
    main()
