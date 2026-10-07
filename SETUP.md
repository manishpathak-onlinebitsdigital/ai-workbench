# Before You Start — One-Time Setup Guide

Welcome! This guide gets your computer ready for the Module 0 labs. **You only do this once.**
No prior coding experience is assumed. Follow the steps for *your* operating system.

> **How long?** About 20–30 minutes the first time.
> **Stuck?** That's normal. Note where you got stuck and bring it to the live session — setup issues are the #1 thing we help with.

---

## What you'll install
1. **Python** (the language our labs are written in)
2. **VS Code** (the editor where you'll write and read code)
3. **Git** (saves and backs up your work — used from Week 2)
4. An **OpenAI API key** (lets your code talk to the AI — needed from Week 1)

---

## Step 1: Install Python (3.11 or newer)

We recommend **Python 3.11 or newer**. (Our code also runs on 3.9+, but newer is smoother.)

### Windows
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click **Download Python 3.12** (big yellow button)
3. Run the installer. **CRITICAL:** on the first screen, check the box that says
   **"Add python.exe to PATH"** before clicking Install. This one checkbox prevents the
   most common beginner problem.
4. Verify: open **Command Prompt** (search "cmd" in the Start menu) and type:
   ```
   python --version
   ```
   You should see `Python 3.12.x`.

### macOS
Many Macs already have an old Python (3.9). That works, but to get a newer one:
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download **Python 3.12 for macOS** and run the installer.
3. Verify: open **Terminal** (press ⌘+Space, type "Terminal") and type:
   ```
   python3 --version
   ```
   You should see `Python 3.12.x` (or `3.9.x` — that's fine too).

> **Note on commands:** Throughout the labs, Windows uses `python` and Mac/Linux uses `python3`.
> Same program, different name. We'll remind you when it matters.

---

## Step 2: Install VS Code (the editor)

1. Go to [code.visualstudio.com](https://code.visualstudio.com/)
2. Download for your OS and install (accept the defaults).
3. Open VS Code. When prompted, install the **Python extension** (search "Python" by Microsoft
   in the Extensions panel on the left). This gives you helpful hints and lets you run code.

---

## Step 3: Install Git (used from Week 2)

### Windows
1. Go to [git-scm.com/download/win](https://git-scm.com/download/win) — download starts automatically.
2. Run the installer. **Accept all the defaults** (just keep clicking Next).
3. Verify: in Command Prompt, type `git --version`. You should see a version number.

### macOS
1. In Terminal, type `git --version`.
2. If Git isn't installed, macOS will pop up a box offering to install it — click **Install**.

---

## Step 4: Get Your OpenAI API Key (needed from Week 1)

Your code needs a "key" to use the AI — like a password that also tracks usage.

1. Go to [platform.openai.com/signup](https://platform.openai.com/signup) and create an account.
2. Add a payment method under **Settings → Billing**, and add a small credit (**$5 is plenty**
   for this entire module — our labs cost only a few cents).
3. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys).
4. Click **Create new secret key**. Copy it immediately — it looks like `sk-...` and is shown
   **only once**. Paste it somewhere safe for now (a private note).

> **Keep it secret.** This key is tied to your billing. Never share it, never post it,
> never put it in a screenshot. In the labs we'll show you exactly how to store it safely.
> If you ever expose it, delete it on that same page and make a new one.

---

## Step 5: Quick Confidence Check

Open your terminal (**Command Prompt** on Windows, **Terminal** on Mac) and run these one at a time.
Each should print a version number, not an error:

**Windows:**
```
python --version
git --version
```

**macOS / Linux:**
```
python3 --version
git --version
```

If both print versions, you're ready. 🎉

---

## Common First-Time Problems

| What you see | What it means | Fix |
|---|---|---|
| `'python' is not recognized` (Windows) | Python wasn't added to PATH | Reinstall Python, check the **"Add to PATH"** box |
| `command not found: python3` (Mac) | Python not installed | Install from python.org (Step 1) |
| `git: command not found` | Git not installed | Do Step 3 |
| You don't see `(.venv)` in your prompt during labs | Environment not activated | Re-run the activate command (the lab shows it) |
| `UnicodeEncodeError` when running the CLI | Old Windows terminal encoding | Our code already handles this; make sure you're on Python 3.7+ |

---

## A Note for Everyone — Whatever Your Background

This module is built for a **mix of people**: some have never written a line of code, others
are software or data engineers. If you're new: **you are not behind.** Every command is shown
on screen, and you can pause the video anytime. Follow the *idea* first; the keystrokes become
muscle memory faster than you'd expect.

If you're experienced: the value is in the *why* behind each choice — the architecture decisions,
the security practices, the provider-agnostic design. Skim the mechanics; focus on the reasoning.

See you in the lab.
