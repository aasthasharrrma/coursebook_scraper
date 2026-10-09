#!/usr/bin/env python3
"""Convert a manually saved CourseBook results table into reviewable JSON.

This module intentionally performs no HTTP requests. Use it only with an HTML
file saved manually from an authorized browser session or with a sanctioned
export. It is a schema-evaluation helper, not a CourseBook web scraper.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class ResultsTableParser(HTMLParser):
    """Small HTML-table parser for locally saved, non-restricted search results."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self._table: list[list[str]] | None = None
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "table":
            self._table = []
        elif tag == "tr" and self._table is not None:
            self._row = []
        elif tag in {"th", "td"} and self._row is not None:
            self._cell = []

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"th", "td"} and self._cell is not None and self._row is not None:
            self._row.append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif tag == "tr" and self._row is not None and self._table is not None:
            if self._row:
                self._table.append(self._row)
            self._row = None
        elif tag == "table" and self._table is not None:
            if self._table:
                self.tables.append(self._table)
            self._table = None


def normalize_header(value: str) -> str:
    return "_".join("".join(ch.lower() if ch.isalnum() else " " for ch in value).split())


def table_to_records(table: list[list[str]]) -> list[dict[str, str]]:
    if len(table) < 2:
        return []
    headers = [normalize_header(value) or f"column_{index + 1}" for index, value in enumerate(table[0])]
    records: list[dict[str, str]] = []
    for row in table[1:]:
        if len(row) != len(headers):
            continue
        records.append(dict(zip(headers, row, strict=True)))
    return records


def extract_records(html: str) -> list[dict[str, str]]:
    parser = ResultsTableParser()
    parser.feed(html)
    candidates = [table_to_records(table) for table in parser.tables]
    candidates = [records for records in candidates if records]
    return max(candidates, key=len) if candidates else []


def build_output(input_path: Path) -> dict[str, Any]:
    records = extract_records(input_path.read_text(encoding="utf-8"))
    return {
        "notice": "Offline extraction from a manually saved or sanctioned source file. Verify fields before use.",
        "source_file": input_path.name,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "record_count": len(records),
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline CourseBook HTML converter; makes no network requests.")
    parser.add_argument("--input", required=True, type=Path, help="Manually saved or sanctioned HTML input")
    parser.add_argument("--output", required=True, type=Path, help="JSON output path")
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(build_output(args.input), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
