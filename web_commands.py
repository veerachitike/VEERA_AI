import webbrowser
from urllib.parse import quote_plus

from speech import speak
from weather import get_weather
from config import sites

def handle_web(c):

    c = c.lower().strip()

    # ---------- GOOGLE SEARCH HELPERS ----------

    if (
        c.startswith("how to")
        or c.startswith("download")
        or c.startswith("install")
    ):

        message = f"Searching Google for {c}"

        speak("Searching Google")

        webbrowser.open(
            f"https://www.google.com/search?q={quote_plus(c)}"
        )

        return message

    # ---------- PREDEFINED SITES ----------

    for name, url in sites.items():

        if f"open {name}" in c:

            message = f"Opening {name}"

            speak(message)

            webbrowser.open(url)

            return message

    # ---------- OPEN WEBSITE ----------

    OPEN_TRIGGERS = [
        "can you open",
        "could you open",
        "please open",
        "open",
        "launch"
    ]

    site = None

    for trigger in OPEN_TRIGGERS:

        if c.startswith(trigger):

            site = c.replace(
                trigger,
                ""
            ).strip()

            break

    if site:

        # Let app_commands handle apps
        APP_NAMES = [
        "calculator",
        "notepad",
        "chrome",
        "edge",
        "brave",
        "browser",
        "internet",
        "music",
        "songs",
        "editor",
        "code",
        "coding app",
        "visual studio",
        "vscode",
        "spotify",
        "task manager",
        "settings",
        "control panel",
        "downloads",
        "documents",
    ]

        if site in APP_NAMES:
            return False

        SPECIAL_SITES = {
            "chatgpt": "https://chatgpt.com",
            "github": "https://github.com",
            "gmail": "https://mail.google.com",
            "youtube": "https://youtube.com",
            "reddit": "https://reddit.com",
            "stackoverflow": "https://stackoverflow.com"
        }

        if site in SPECIAL_SITES:

            message = f"Opening {site}"

            speak(message)

            webbrowser.open(
                SPECIAL_SITES[site]
            )

            return message

        if " " not in site:

            message = f"Opening {site}"

            speak(message)

            webbrowser.open(
                f"https://www.{site}.com"
            )

            return message

    # ---------- SEARCH ----------

    if c.startswith("search "):

        query = c.replace(
            "search ",
            ""
        ).strip()

        message = (
            f"Searching Google for {query}"
        )

        speak(message)

        webbrowser.open(
            f"https://www.google.com/search?q={quote_plus(query)}"
        )

        return message

    # ---------- WEATHER ----------

    if "weather" in c:

        city = "chennai"

        if "weather in" in c:

            city = c.split(
                "weather in"
            )[-1].strip()

        result = get_weather(city)

        speak(result)

        return result

    return False