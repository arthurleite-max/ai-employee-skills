# Technical basics

Only what a small-business site needs. Say what you checked and how.

| Check | Good | Finding when |
|---|---|---|
| Title | Unique per page, about 50–60 characters, says what and where | Missing, duplicated, "Home", "Untitled" |
| Meta description | About 140–160 characters, a reason to click | Missing or duplicated |
| Headings | One H1 per page, H2/H3 in order | No H1, several H1s, skipped levels used for styling |
| Images | Meaningful `alt` text; decorative ones `alt=""` | `alt` missing; file names as alt ("IMG_2033.jpg") |
| Links | Descriptive text; internal links resolve; external open fine | 404/500, `href="#"` on a CTA, "click here" |
| Language | `<html lang="…">` set | Missing |
| Mobile | `<meta name="viewport" …>`; no horizontal scroll; tap targets ≥ 44 px where possible | Missing viewport, tiny buttons |
| Contrast | Body text ≥ 4.5:1, large text ≥ 3:1 | Light grey on white, text on busy photos |
| Forms | Labels, required marked, privacy notice | Placeholder-only fields, no notice |
| HTTPS | All resources over https | `http://` images, scripts or forms |
| Structured data (local business) | Name, address, phone, hours consistent with the page | Different from the page |
| Cookies and tracking | Consent where the law requires it | Tracking without consent banner where needed |
| Speed | Images sized for the web (usually under ~300 KB each), few heavy scripts | Multi-MB images, many third-party scripts |

## The checker

`scripts/sitecheck.py` covers the mechanical part:

```
python sitecheck.py https://example.com --max-pages 30 --year 2026 > report.md
python sitecheck.py ./site-folder --year 2026 --json findings.json
```

It reports: status codes and broken internal links (and external links with `--external`), titles,
descriptions, H1 count, images without alt, missing `lang`/viewport, inputs without labels, `http://`
resources, old years and "©" years, placeholder text, `tel:`/`mailto:`/WhatsApp links found, phone
numbers that differ between pages, large images (when the server reports size), and comments or hidden
text that address an AI. It never submits forms and only follows links on the same site.

Treat its output as candidates: confirm in context before reporting.
