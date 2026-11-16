# Audit, test, release

## 1. Package audit

`python scripts/package.py my-skill --forbid forbid.txt [--words words.txt]`

| Blocks the zip | Warns |
|---|---|
| Missing required files · `name` ≠ folder or not kebab-case · description missing or > 1,024 · compact edition > 8,000 · a file cited in `SKILL.md` missing · leftover TODO · control characters · secrets · local paths · forbidden terms (internal names, real clients, test-case data) · leftover words (e.g. another language) · imports outside the standard library | No tutorial · scripts that can reach the network · emails or phone numbers outside `.example` · package above 5 MB |

Caches (`__pycache__`, `.DS_Store`) are never packed.

## 2. Test before release

- A fictional case with one trap per rule, expected values computed outside, must-pass checks decided first.
- At least two targets, including the weakest environment real users have (a free chat, paste only).
- Scripted follow-ups: pressure, correction, cold start.
- Every failure: cause → smallest fix → re-test in a fresh conversation.
- Keep the test kit and results **outside** the public folder.

## 3. Release

Version in the front matter · zip from the audit · README and tutorial checked by someone non-technical ·
known limits written · licence confirmed by the owner · published only where the owner decided.
