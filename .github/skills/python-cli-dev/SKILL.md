---
name: python-cli-dev
description: "Python CLI development conventions for pdf-extraction-tool. Use when: editing extract_pdf.py, adding CLI arguments, adding new backends, fixing CLI errors, or implementing new CLI features. Covers argparse patterns, backend dispatch, error handling, and entry point configuration."
---

# Python CLI Development

## Project Structure

```
extract_pdf.py          # Main CLI module (single-file)
tests/                  # pytest tests
pyproject.toml          # Project metadata, deps, entry points
```

## Entry Point

Defined in `pyproject.toml`:
```toml
[project.scripts]
extract-pdf = "extract_pdf:main"
```

## CLI Arguments Pattern

Always use `argparse` with this pattern:
- `pdf_path` — positional, `type=Path`
- `--backend` — choices `['pypdf2', 'pdfminer']`, default `pypdf2`
- `--password` — optional string for encrypted PDFs

## Backend Architecture

- **pypdf2** (default, required): `PyPDF2>=3.0.0`
- **pdfminer** (optional): `pdfminer.six>=20221105`, installed via `[backends]` extra
- New backends: add a new `extract_text_<name>()` function and extend the `choices` list in argparse

## Error Handling Rules

1. File not found → `parser.error(...)` (exits with code 2)
2. Encrypted PDF without password → print to stderr, `sys.exit(1)`
3. Wrong password → print to stderr, `sys.exit(1)`
4. Corrupt/non-PDF file → catch `PdfReadError`, print to stderr, `sys.exit(1)`
5. Missing optional backend → print install command to stderr, `sys.exit(1)`

## Code Style

- **Formatter**: Ruff format (single quotes, line-length 100)
- **Linter**: Ruff (E, F, I, UP rules)
- **Type checker**: mypy (strict, excludes `tests/`)
- **Pre-commit**: `ruff --fix` + `ruff format`

## Testing

- Framework: pytest
- PDF fixture generation: reportlab
- Place tests in `tests/test_<module>.py`
- Use `_create_*` helper functions for PDF fixtures