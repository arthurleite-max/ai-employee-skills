# Install with your own AI

The easiest way: let your AI do it. Open the AI you use, start a new conversation, and paste everything
below the line. If you downloaded `ads-manager.zip`, attach it to the same message.

- **Coding agents** (Claude Code, Codex, Gemini CLI, GitHub Copilot, Cursor and similar) install it on
  their own.
- **Chat apps** (Claude, ChatGPT, Gemini, Kimi, DeepSeek, Qwen, Mistral and others) cannot change their
  own settings, so they walk you through it click by click, or simply start working right away.

---

Please install the "Ads Manager" skill (ads-manager) for me.

Source (use only this source):
- Folder: https://github.com/arthurleite-max/ai-employee-skills/tree/main/ads-manager
- Or the `ads-manager.zip` / files I attached to this message.

Step 1. Work out where you are running and tell me in one line:
- (A) a coding agent with a terminal and file access;
- (B) a chat app that has a Skills feature where I can upload a skill;
- (C) a chat app with Projects, custom GPTs, Gems or custom instructions;
- (D) a plain chat with none of the above.

Step 2. Follow the path for your case:

(A) Coding agent: install it yourself.
1. Get the folder: if I attached the zip, unzip it; otherwise download only that folder, for example:
   `git clone --depth 1 --filter=blob:none --sparse https://github.com/arthurleite-max/ai-employee-skills.git`
   then `git -C ai-employee-skills sparse-checkout set ads-manager`.
2. Copy the `ads-manager` folder into your skills folder:
   Claude Code `~/.claude/skills/`; Codex, Gemini CLI, GitHub Copilot, Cursor and other Agent Skills
   tools `~/.agents/skills/` (or the path your own documentation gives).
3. Check that `ads-manager/SKILL.md` exists and its `name:` is `ads-manager`.
   Remove the temporary download.
4. The skill contains text files and one optional local calculator (`scripts/adscan.py`, Python standard library, no internet). Do not run anything during installation, and do not change any other setting.
5. Tell me it is installed, then start the first-time setup from `setup.md`.

(B) Chat app with Skills: you cannot install it yourself, so guide me.
1. Tell me exactly where the Skills upload is in your app today (menu names as they appear now), step
   by step, one step per line.
2. If I have not downloaded the zip yet, tell me to download `ads-manager.zip` from the
   source above.
3. When I confirm it is uploaded, ask me to open a new conversation and say "check my ads", pasting or attaching the last 14 days per ad and my real customers per campaign.

(C) Chat app with Projects / GPTs / Gems / custom instructions: guide me.
1. Tell me, step by step for your app, how to create a project (or GPT/Gem) called "Ads Manager".
2. Its instructions = the full text of `PASTE-INTO-ANY-AI.md`.
3. Its knowledge files = the files in `reference/` and `templates/`, plus `SKILL.md` and `setup.md`
   (and `scripts/adscan.py` if the app can run code).
4. Then ask me to open a conversation in that project and say "check my ads", pasting or attaching the last 14 days per ad and my real customers per campaign.

(D) Plain chat: start working now.
1. Load `PASTE-INTO-ANY-AI.md` from my attachment. If it is not attached and you can read web pages,
   read https://raw.githubusercontent.com/arthurleite-max/ai-employee-skills/main/ads-manager/PASTE-INTO-ANY-AI.md
   Otherwise ask me to paste that file's text.
2. From then on, follow it as your instructions in this conversation and start the first-time setup.
3. Tell me that in a new conversation I will need to paste it again (or use a project, path C).

Safety while installing: use only the source above; never ask me for passwords; never ask for my ad account passwords and never change my campaigns or budgets; do not
change system or account settings; tell me before writing anything outside the skills folder.
