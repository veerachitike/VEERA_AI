import os
from rapidfuzz import fuzz
from speech import speak


APPS = {
    "calculator": "calc",
    "notepad": "notepad",
    "chrome": "chrome",
    "edge": "msedge",
    "brave": "brave"
}

CLOSE_APPS = {
    "notepad": "notepad.exe",
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "brave": "brave.exe"
}


def similar(command, text, score=75):
    return fuzz.partial_ratio(command, text) >= score


def handle_apps(c):

    print("handle_apps received:", c)

    c = c.lower().strip()

    # ---------- OPEN APPS ----------

    if any(word in c for word in ["open", "launch", "start"]):

        # Direct Match

        for app, command in APPS.items():

            if app in c:

                try:

                    print("MATCHED:", app)

                    speak(f"Opening {app}")

                    os.system(
                        f"start {command}"
                    )

                    return f"Opening {app}"

                except Exception as e:

                    print("Open Error:", e)

                    return f"Failed to open {app}"

        # Fuzzy Match

        best_app = None
        best_score = 0

        for app in APPS:

            score = fuzz.partial_ratio(
                app,
                c
            )

            print(
                f"APP: {app} | SCORE: {score}"
            )

            if score > best_score:

                best_score = score
                best_app = app

        if best_app and best_score >= 80:

            try:

                speak(f"Opening {best_app}")

                os.system(
                    f"start {APPS[best_app]}"
                )

                return f"Opening {best_app}"

            except Exception as e:

                print("Open Error:", e)

                return f"Failed to open {best_app}"

    # ---------- CLOSE APPS ----------

    for app, process in CLOSE_APPS.items():

        if (
            c.strip() == f"close {app}"
            or similar(c, f"exit {app}", 85)
            or similar(c, f"quit {app}", 85)
        ):

            try:

                speak(f"Closing {app}")

                os.system(
                    f"taskkill /f /im {process}"
                )

                return f"Closing {app}"

            except Exception as e:

                print("Close Error:", e)

                return f"Failed to close {app}"

    # ---------- CLOSE CALCULATOR ----------

    if "close calculator" in c:

        try:

            speak("Closing calculator")

            os.system(
                "taskkill /f /im CalculatorApp.exe"
            )

            return "Closing calculator"

        except Exception as e:

            print("Close Error:", e)

            return "Failed to close calculator"

    return False