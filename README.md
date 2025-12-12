
# **Casa Squire Bot**
*A personal Telegram assistant for remotely scheduling Windows shutdowns and startups via WOL.*

---

## 🏷️ **Badges**

![Python](https://img.shields.io/badge/Python-3.11+-0c0c0c?style=for-the-badge&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-0c0c0c?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-0c0c0c?style=for-the-badge&color=4caf50)
![License](https://img.shields.io/badge/License-MIT-0c0c0c?style=for-the-badge)

---

## 📌 **Overview**

Casa Squire Bot is a private-use Telegram bot that allows the owner to remotely schedule a Windows shutdown.

When sending `/shutdown`, the bot displays:

- Shutdown **now**
- Shutdown in **1–4 hours**
- **Cancel** scheduled shutdown

Only owner IDs are allowed to access the bot.  
All other users are ignored via middleware.

---

## 🧩 **Requirements**

- Windows **10/11**, or WSL with access to `cmd.exe`
- Python **3.11+** in PATH
- Telegram bot token (`BOT_TOKEN`)
- Owner user ID(s) (`OWNER_IDS` in `.env`)

---

## 📁 **Project Structure**

| File | Description |
|------|-------------|
| `install_windows.bat` | Creates venv, installs dependencies, asks for token & owner ID, writes `.env`, and registers Task Scheduler autostart. |
| `run_windows.bat` | Activates the venv and launches `python bot.py`. |
| `bot.py` | Main entry point (Aiogram 3). |
| `pyproject.toml` / `poetry.lock` | Dependency specification (Poetry). |
| `requirements.txt` | Exported dependencies (`poetry export`). |

---

## 🛠 **Installation (Windows)**

1. Ensure Python **3.11+** is installed.
2. Run:

```
install_windows.bat
```

The script will:

- Create a virtual environment  
- Install dependencies  
- Ask for `BOT_TOKEN` and `OWNER_IDS`  
- Write `.env`  
- Create Task Scheduler autostart job (`CasaSquireBot`) that runs `run_windows.bat`

> If autostart fails, run the installer **as Administrator**.

---

## 🚀 **Manual Launch**

```
run_windows.bat
```

Or:

```powershell
.\venv\Scripts\activate
python bot.py
```

---

## 🐧 **Running Under WSL**

WSL can execute `.bat` using:

```
cmd.exe /C install_windows.bat
```

But Task Scheduler cannot be configured from Linux.

WSL Instructions:

```bash
pip install -r requirements.txt
echo "BOT_TOKEN=xxx" > .env
echo "OWNER_IDS=123456789" >> .env
python bot.py
```

Ensure:

- `cmd.exe` is accessible (usually `/mnt/c/Windows/System32/cmd.exe`)
- Your user has permission to run Windows shutdown commands

---

## ⚠️ **Limitations**

- Works **only in private chats**
- Only for users listed in `OWNER_IDS`
- Shutdown uses:

```
cmd.exe /c shutdown
```

Therefore, the bot is **not compatible with pure Linux or macOS**  
(WSL works only partially).

- Cancellation is only possible while a shutdown timer is active.

---

## 🗺️ **Roadmap**

- [ ] Desktop app launcher (PyQt / Tkinter)
- [ ] Windows installer (.exe)
- [ ] Notification center for shutdown timers
- [ ] Localization (i18n)
- [ ] Web dashboard for controlling bot

---

## 📜 **License**

MIT License — feel free to use and modify.
