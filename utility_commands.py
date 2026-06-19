import os

from datetime import datetime

from speech import speak


IGNORE_WORDS = {
    "uh",
    "umm",
    "hmm",
    "ok",
    "okay",
    "ah",
    "eh"
}


def handle_utility(c):

    # HELP
    if c.strip() == "help":

        message = (
            "I can open applications, websites, "
            "play music, take screenshots, "
            "search Google, and answer questions."
        )

        speak(message)

        return message

    # SCREENSHOT
    if (
        "take screenshot" in c
        or "take a screenshot" in c
        or "capture screenshot" in c
    ):

        import pyautogui

        os.makedirs(
            "Screenshots",
            exist_ok=True
        )

        filename = os.path.join(
            "Screenshots",
            datetime.now().strftime(
                "screenshot_%Y%m%d_%H%M%S.png"
            )
        )

        pyautogui.screenshot().save(
            filename
        )

        speak("Screenshot taken")

        return (
            f"Screenshot saved successfully.\n"
            f"File: {os.path.basename(filename)}"
        )

    # COMMAND HISTORY
    if "show command history" in c:

        try:

            with open(
                "logs/commands.log",
                "r",
                encoding="utf-8"
            ) as file:

                history = file.readlines()

            recent = history[-10:]

            speak(
                "Showing last commands"
            )

            if recent:

                return (
                    "Recent Commands:\n\n"
                    + "".join(recent)
                )

            return "No command history found"

        except Exception:

            speak(
                "No command history found"
            )

            return "No command history found"

    # IGNORE FILLER WORDS
    if c.strip().lower() in IGNORE_WORDS:

        return False

    # VERY SHORT INPUT
    if len(c.strip()) <= 2:

        speak(
            "Please say that again"
        )

        return "Please say that again"

    return False