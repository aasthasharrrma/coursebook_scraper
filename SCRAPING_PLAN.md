# CourseBook Data Acquisition Plan

## Purpose

Provide Assessment Helper with current course and section information after the Nebula API route could not be used. This plan distinguishes planning and offline processing from permission-required automated collection.

## Access decision

**Current decision: do not scrape CourseBook automatically.** The site’s public JavaScript includes a statement that automated access by robots, spiders, or scrapers requires prior express written permission. The application also uses CAPTCHA controls. The project will not circumvent those controls, replay browser requests, automate a login, or call undocumented internal endpoints.

## Approval path

1. Send the request in `docs/ACCESS_REQUEST_TEMPLATE.md` to CourseBook support.
2. Ask first for an approved API, export, or bulk data feed; it is preferable to screen scraping.
3. If automation is approved, store the written approval in the project’s private records and record: allowed routes, fields, terms, refresh frequency, request-rate limit, required attribution, retention limits, and a support contact.
4. Implement only the exact approved scope. Do not expand the data collection scope based on inferred permission.

## Interim method: manual browser export plus offline conversion

Until approval is received, a team member may manually use the public CourseBook interface and save a small, relevant results page as HTML. `src/coursebook_ingest.py` parses that local file only; it has no networking code. This keeps the team moving while preserving the site’s access boundary.

Suggested pilot scope:

| Item | Pilot decision |
| --- | --- |
| Term | One currently relevant term |
| Prefixes | Start with the project’s needed academic area, such as CS |
| Collection method | Manual browser search and local HTML save |
| Frequency | One-time pilot; no scheduled refreshes |
| Sensitive/restricted content | Exclude login-only pages, syllabi, evaluations, grades, and student information |
| Output | Local JSON for schema evaluation only |

## Minimum data contract

The internal model should preserve source values and tolerate missing fields.

| Field | Why Assessment Helper needs it |
| --- | --- |
| `term` | Identify the academic period |
| `course_prefix` and `course_number` | Course identity and filtering |
| `course_title` | Student-facing course label |
| `section` | Distinguish offerings of the same course |
| `instructor_name` | Display only; not a stable identity without an official identifier |
| `department` | Filtering and grouping |
| `schedule`, `location`, `modality` | Planning context when present |
| `source_url` / `source_id` | Traceability without inventing identifiers |
| `synced_at` | Freshness indicator |

## Implementation sequence after approval

1. **Contract check:** review the approved interface and update the parser/adapter to its documented fields.
2. **Tiny smoke test:** make one approved request for one term and one prefix; capture only sanitized diagnostics.
3. **Schema validation:** compare returned fields with the minimum data contract and document null/missing behavior.
4. **Rate-limited pilot:** use the written rate limit; otherwise pause and obtain an explicit limit rather than guessing.
5. **Adapter integration:** keep provider-specific code in one backend module. The browser must never directly call CourseBook or expose credentials.
6. **Quality review:** confirm duplicates, term codes, empty values, stale data, and display formatting.
7. **Release decision:** document coverage, refresh process, error handling, and limitations before enabling a student-facing feature.

## Stop conditions

Stop collection and contact the source owner if any of these occur:

- Written permission has not been received.
- CAPTCHA, login, access errors, or anti-automation messages appear.
- The site’s policy or robots guidance changes.
- The requested scope would include restricted content or personal/student information.
- The source has not provided a rate limit for an automated workflow.

## Testing and evidence

- Unit-test local HTML parsing against synthetic fixtures only.
- Maintain a sample manifest with source filename, manual capture date, requested term/prefix, and parser version.
- Never commit live saved HTML containing restricted content or personally identifiable information.
- Record a validation checklist before moving data into the application database.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Access policy violation | No live automation until written authorization; use approved feeds or offline manual exports. |
| Changing HTML markup | Keep parsing isolated and test against fixtures; revalidate after any site change. |
| Incomplete or stale data | Store `synced_at`, surface limits, and validate term coverage. |
| Incorrect field mapping | Preserve raw headers/values in pilot data and review mappings before release. |
| Credential or personal-data exposure | Avoid login flows and restricted fields; keep any future credentials backend-only. |
