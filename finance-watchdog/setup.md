# Setup: the first conversation

Goal: in about 10 minutes, a filled-in profile, a first audit of the statements the owner brings, and the
first decisions taken. Talk to the owner in their language.

## 1. What to bring

Ask for the statements first, because everything else is easier with them on the table:

- **Best:** CSV, OFX or XLSX exports of the business account and every card, for the last **3 months**
  (12–13 months finds annual renewals too). In most banking apps: Statement → Export → CSV or OFX.
- **Fine:** PDF statements, screenshots or copied lines.
- **Never:** passwords, codes, full card numbers. "I don't need your login, only the statement file."

If nothing is available yet, do the questions now and the audit when the files arrive.

## 2. The minimum questions

Short blocks; accept "skip" for any. Anything not answered keeps the template's default
(`templates/profile.example.md`).

1. Your name, the business, what it does in one sentence. Business, household, or both?
2. Currency, language, and how you write dates (DD/MM or MM/DD).
3. Which accounts and cards exist, who uses each, and which are business only? (last 4 digits only)
4. Your own accounts and investments (so transfers to them are not counted as spending).
5. Main suppliers and fixed costs: rent, payroll dates, accountant, taxes.
6. What must **never** be cut (the till, the website, payroll software…)?
7. Anything you cancelled recently, or a refund you are waiting for?
8. From what amount should an unknown charge alert you? Should possible fraud reach you immediately?
9. Which day do you want the weekly report, and where (chat, web page, WhatsApp, email)?

## 3. First audit

Run Mode 2 with what the owner brought. Then ask only what the data cannot answer, for the top items:
"Is GymOne personal?", "Who uses CloudHost?", "Two video-call tools: which stays?". Record every answer
in the profile or the merchant map.

## 4. Save the files

At level 3, write `finance-watchdog-data/profile.md`, `finance-watchdog-data/memory.json` (merchant map,
recurring list, baselines, decisions) and `finance-watchdog-data/reports/`. Add the data folder to any
version-control ignore list: financial data never goes into a repository.

At levels 1 and 2, hand back the profile and the memory in two code blocks: "Keep these two texts.
Next time, paste or attach both with the new statement."

## 5. Schedule (if the owner wants)

Suggest the weekly run on the chosen day. The platform creates it (scheduled tasks or an external
automation). If it cannot, the owner opens the conversation, pastes the week's statement and says
"weekly report". The scheduled run only reads and reports (see `SKILL.md` → "Scheduled run").
