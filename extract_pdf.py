import argparse
from pathlib import Path

import PyPDF2


def main() -> None:
    parser = argparse.ArgumentParser(description='Extract text from a PDF file.')
    parser.add_argument('pdf_path', type=Path, help='path to the PDF file')
    args = parser.parse_args()

    if not args.pdf_path.is_file():
        parser.error(f'PDF file not found: {args.pdf_path}')

    reader = PyPDF2.PdfReader(args.pdf_path)
    print(f'Number of pages: {len(reader.pages)}')
    print('=' * 80)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f'--- Page {i + 1} ---')
        print(text)
        print('=' * 80)


if __name__ == '__main__':
    main()
