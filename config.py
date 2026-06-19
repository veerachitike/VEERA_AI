import os

from dotenv import load_dotenv

load_dotenv()
# ─────────────────────────────────────────────
# API KEYS
# ─────────────────────────────────────────────

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# ─────────────────────────────────────────────
# WEBSITES
# ─────────────────────────────────────────────

SITES = {
    "google": "https://google.com",
    "youtube": "https://youtube.com",
    "instagram": "https://instagram.com",
    "facebook": "https://facebook.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chatgpt.com",
    "reddit": "https://reddit.com",
    "stackoverflow": "https://stackoverflow.com"
}


# Backward compatibility
sites = SITES


# ─────────────────────────────────────────────
# VOICE ASSISTANT
# ─────────────────────────────────────────────

WAKE_WORDS = [
    "hey veera",
    "veera"
]

ACTIVE_TIMEOUT = 20


# ─────────────────────────────────────────────
# FILES & FOLDERS
# ─────────────────────────────────────────────

SCREENSHOT_FOLDER = "Screenshots"

LOG_FOLDER = "logs"

MEMORY_FILE = "memory.txt"


# ─────────────────────────────────────────────
# WEATHER
# ─────────────────────────────────────────────

DEFAULT_CITY = "chennai"


# ─────────────────────────────────────────────
# AUDIO
# ─────────────────────────────────────────────

VOICE_NAME = "en-US-JennyNeural"

VOICE_RATE = 170