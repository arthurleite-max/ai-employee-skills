# The compact edition (PASTE-INTO-ANY-AI.md)

The file a user pastes as the first message of any chat. It must work **alone**, under **8,000
characters** (leave room for the user's data in the same message).

## Shape

1. One paragraph: who you are, the job, languages.
2. "If SKILL.md and the reference files are attached, use them; these instructions are enough on their own."
3. **Rules that never change**: numbered, concrete, testable (the non-negotiable rules + money format).
4. **First conversation**: the setup questions in one paragraph, then "write the profile for approval".
5. **Main task (do it in this order)**: numbered steps, tables first, summary last, one question.
6. Other modes in one line each, if any.
7. "If you can run code: python scripts/… " and "Offer at most three next steps."

## Checks

- Every rule from `SKILL.md` that a test can fail is here (shortened, not dropped).
- No reference to a file the user will not have.
- Count the characters; cut words, not rules.
