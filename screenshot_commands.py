import os
import pyautogui
from datetime import datetime
from speech import speak
from notifications import notify


def handle_screenshot(c):

    c = c.lower().strip()

    if (
        "take screenshot" in c
        or "capture screen" in c
        or "take a screenshot" in c
    ):

        os.makedirs(
            "Screenshots",
            exist_ok=True
        )

        filename = datetime.now().strftime(
            "Screenshots/screenshot_%Y%m%d_%H%M%S.png"
        )

        pyautogui.screenshot(
            filename
        )

        notify(
            "VEERA Screenshot",
            "Screenshot saved successfully"
        )

        message = (
            "Screenshot saved"
        )

        speak(message)

        return message

    return False