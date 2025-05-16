# LaTeX to Markdown Converter

This script converts LaTeX content to Markdown format, optimized for use in Obsidian. It processes various LaTeX elements into clean, readable Markdown.

## Features

- Converts LaTeX sections, subsections, and subsubsections to Markdown headers.
- Handles `align*`, `equation*`, and inline math, converting them to Markdown math blocks.
- Replaces `&=` with `=` in `align*` environments for proper Markdown rendering.
- Extracts title, author, and date from the LaTeX preamble, if provided.
- Supports basic list conversion from LaTeX `itemize` environments.
- Ignores LaTeX-specific commands like `\newpage`, `\maketitle`, and `\tableofcontents`.

## Usage

Run the script from your terminal with:

```bash
python convert_latex_to_markdown.py input_file.txt
```

- `input_file.txt`: Your LaTeX input file.

The script outputs a Markdown file with the same name but a `.md` extension (e.g., `input_file.md`).

## Requirements

- Python 3.x


*Note: This script works best with basic LaTeX documents. Complex or nested environments may require additional tweaks.*
