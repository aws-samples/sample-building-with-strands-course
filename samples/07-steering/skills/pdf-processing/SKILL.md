---
name: pdf-processing
description: Extract text and tables from PDF files
---
# PDF Processing

When asked to extract content from a PDF:

1. Use `shell` to run `scripts/extract.py` on the target file
2. Use `file_read` to review the extracted output
3. Summarize the extracted content for the user

For tables, use the `--tables` flag with the extraction script.
For images, use the `--images` flag to extract embedded images.

Always report the page count and any extraction errors.
