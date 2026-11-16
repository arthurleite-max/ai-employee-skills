# How to install Ads Manager

Pick the AI you use. It takes about one minute and works on free plans.

> The screenshots show the **Executive Assistant**. For **Ads Manager** every step is identical: only the name changes.

- [Claude: install it for good](#claude-install-it-for-good)
- [ChatGPT: copy, paste, and save it in a Project](#chatgpt-copy-paste-and-save-it-in-a-project)
- [Make it work like an employee](#make-it-work-like-an-employee-chatgpt-free)
- [DeepSeek and any other chat](#deepseek-and-any-other-chat)
- [Coding agents](#coding-agents)

---

## Claude: install it for good

![Watch: from GitHub to Claude](../guide-images/gif-claude.gif)

**1. Download the skill: [ads-manager.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/ads-manager.zip)**. Do **not** unzip it.
You can also click **download zip** next to Ads Manager in the [list of employees](https://github.com/arthurleite-max/ai-employee-skills#readme).

![Download link on GitHub](../guide-images/github-3-download.jpg)

**2.** In Claude, click your name (bottom left) → **Settings** → **Capabilities**. **Create and edit files** must be on (it is on by default).

![Claude settings, Capabilities](../guide-images/claude-1-capabilities.jpg)

**3.** Still in Settings: **Customize** → **Skills** tab → **+ Add** → **Upload skill**.

![Add, Upload skill](../guide-images/claude-2-add-upload.jpg)

**4.** Click the box and choose **ads-manager.zip** (you can add several employees at once).

![Upload box](../guide-images/claude-3-choose-zip.jpg)

**5.** Check the preview and click **Upload**.

![Preview and Upload button](../guide-images/claude-5-upload.jpg)

**6.** Done. The switch next to the name must be on.

![Skill installed](../guide-images/claude-6-installed.jpg)

**7.** Open a new chat and say: **Use my Ads Manager skill: check my ads**. You will see *Loaded skill*.

Have this ready: pasting or attaching the last 14 days per ad and your real customers per campaign.

![Loaded skill](../guide-images/claude-7-loaded.jpg)

> Name the skill in your first message: a short phrase alone can be taken as small talk.

---

## ChatGPT: copy, paste, and save it in a Project

![Watch: from GitHub to ChatGPT](../guide-images/gif-chatgpt.gif)

**1.** Here on GitHub, open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)** (it is in this folder).

![The skill folder on GitHub](../guide-images/github-2-folder.jpg)

**2.** Click the **Copy raw file** button (two squares, top right of the file). The whole text is now copied.

![Copy raw file button](../guide-images/github-4-copy-raw.jpg)

**3.** Open [chatgpt.com](https://chatgpt.com), click in the message box, paste (**Ctrl+V**, Mac **⌘V**) and send.

![Pasted into ChatGPT](../guide-images/chatgpt-1-paste.jpg)

**4.** It introduces itself and starts a short setup. Answer in a few words or type "skip".

Have this ready: pasting or attaching the last 14 days per ad and your real customers per campaign.

![First answer](../guide-images/chatgpt-2-reply.jpg)

### Keep it for good (free): save it in a Project

So you never paste again:

![Watch: saving it in a Project](../guide-images/gif-chatgpt-project.gif)

**5.** In the sidebar, hover **Projects** and click **+**. Name it **Ads Manager** and click **Create project**.

![New project](../guide-images/chatgpt-4-name.jpg)

**6.** Click **⋯** next to the project name → **Project settings**.

![Project settings](../guide-images/chatgpt-5-settings.jpg)

**7.** Paste the same text into **Instructions** and click **Save**.

![Instructions pasted](../guide-images/chatgpt-6-instructions.jpg)

**8.** From now on, open the project and say: **check my ads**.

![Using it inside the project](../guide-images/chatgpt-7-use.jpg)

---

## Make it work like an employee (ChatGPT, free)

Let it run on its own. Nothing is ever sent without your "yes".

### Your files

When it runs, attach your Meta and Google Ads exports in the chat (paperclip). On **ChatGPT Plus** you can instead connect **Google Drive** once (sidebar → **Plugins** → Google Drive) and keep the files there; the free plan does not include Google Drive.

### Make it run on its own

![Watch: scheduling it](../guide-images/gif-chatgpt-schedule.gif)

1. In the sidebar, click **Scheduled**.

![Scheduled](../guide-images/chatgpt-12-scheduled.jpg)

2. Type this (change the time if you like) and press Enter:

```
Every weekday at 7:30 AM (my time zone): act as my Ads Manager (the instructions in my Ads Manager project) and ask me for the latest Meta and Google Ads numbers, review my ads and tell me what to change. Never send anything.
```

![Typing the task](../guide-images/chatgpt-13-task.jpg)

3. ChatGPT confirms the schedule. Click **Run now** once to see the result right away.

![Task scheduled](../guide-images/chatgpt-14-task-created.jpg)

---

## DeepSeek and any other chat

![Watch: from GitHub to DeepSeek](../guide-images/gif-deepseek.gif)

**1.** Copy the text the same way: open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)** → **Copy raw file**.

**2.** Open [chat.deepseek.com](https://chat.deepseek.com), paste and send. DeepSeek turns long text into a small file card: that is normal.

![Pasted into DeepSeek](../guide-images/deepseek-1-paste.jpg)

**3.** It introduces itself and starts the setup.

Have this ready: pasting or attaching the last 14 days per ad and your real customers per campaign.

![First answer in DeepSeek](../guide-images/deepseek-2-reply.jpg)

> DeepSeek has no projects or skills: each new chat starts from zero, so paste the text again. The same works on Gemini (paste it into a *Gem* to keep it), Qwen, Kimi, Mistral and others.

---

## Coding agents

Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and similar: copy the text of [INSTALL.md](INSTALL.md) into the agent and send. It downloads only this folder, copies it to its skills folder (`~/.claude/skills/` or `~/.agents/skills/`) and starts the setup.

---

**Safety:** never type passwords, card numbers or bank logins into any AI. This employee is built to refuse them.
