# UTD CourseBook Research and Offline Ingestion

This repository supports the Assessment Helper capstone project's course-data research after the Nebula API access path did not produce a usable integration.

## Important access boundary

The official [UT Dallas CourseBook](https://coursebook.utdallas.edu/) is the authoritative source being evaluated. Its publicly delivered JavaScript states that robots, spiders, and scrapers must not access the website without prior express written permission. This project therefore **does not send automated requests to CourseBook**, does not bypass CAPTCHA, and does not include a live crawler.

Use one of these approved paths:

1. Obtain written permission from UT Dallas / CourseBook support before building or running any live automation.
2. Use the offline ingestion tool on an HTML file that a team member saved manually from a normal browser session.
3. Prefer a university-provided export, data feed, or API if one becomes available.

Questions about CourseBook can be directed to the support address shown on the website: `wat@utdallas.edu`.

## What is included

- `SCRAPING_PLAN.md` — permission-first acquisition plan, scope, schema, testing plan, and stop conditions.
- `docs/ACCESS_REQUEST_TEMPLATE.md` — ready-to-send request for written authorization or an approved data feed.
- `src/coursebook_ingest.py` — an **offline-only** converter for manually saved CourseBook search-result HTML.
- `tests/` — tests and a synthetic fixture. No test contacts CourseBook.

## Offline workflow

1. In a normal browser, search CourseBook for a small, authorized scope (for example, one term and one prefix).
2. Save the results page as an HTML file. Do not collect login-only content, syllabi, evaluations, or any data restricted by the site.
3. Run the converter locally:

```bash
python3 src/coursebook_ingest.py --input /path/to/saved-results.html --output data/coursebook-results.json
```

4. Inspect the JSON before using it in Assessment Helper. The converter records the input filename and extraction time but does not claim that parsed fields are official or complete.

## Development

The project uses only the Python standard library.

```bash
python3 -m unittest discover -s tests -v
```

## Current status

No live CourseBook scraping has been performed. Authenticated or automated collection remains blocked until written permission or an approved data-access route is received.

## Sources

- [UT Dallas CourseBook](https://coursebook.utdallas.edu/)
- [CourseBook robots.txt](https://coursebook.utdallas.edu/robots.txt)
- [CourseBook support and official site information](https://coursebook.utdallas.edu/)
