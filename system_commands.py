import os

from speech import speak
from system_info import (
    get_battery,
    get_cpu,
    get_ram,
    get_system_status
)

PENDING_ACTION = None
print("SYSTEM_COMMANDS FILE LOADED")

def handle_system(c):

    global PENDING_ACTION

    c = c.lower().strip()

    # ---------- LOCK COMPUTER ----------

    if "lock computer" in c:

        message = "Locking computer"

        speak(message)

        os.system(
            "rundll32.exe user32.dll,LockWorkStation"
        )

        return message

    # ---------- CANCEL PENDING ACTION ----------

    if PENDING_ACTION:

        if c in [
            "no",
            "cancel",
            "cancel action"
        ]:

            PENDING_ACTION = None

            message = "Action cancelled"

            speak(message)

            return message

    # ---------- SHUTDOWN ----------

    if "shutdown computer" in c:

        PENDING_ACTION = "shutdown"

        message = (
            "Are you sure? Say confirm shutdown."
        )

        speak(message)

        return message

    # ---------- RESTART ----------

    if "restart computer" in c:

        PENDING_ACTION = "restart"

        message = (
            "Are you sure? Say confirm restart."
        )

        speak(message)

        return message

    # ---------- CONFIRM SHUTDOWN ----------

    if (
        c == "confirm shutdown"
        and PENDING_ACTION == "shutdown"
    ):

        PENDING_ACTION = None

        message = "Shutting down computer"

        speak(message)

        os.system(
            "shutdown /s /t 1"
        )

        return message

    # ---------- CONFIRM RESTART ----------

    if (
        c == "confirm restart"
        and PENDING_ACTION == "restart"
    ):

        PENDING_ACTION = None

        message = "Restarting computer"

        speak(message)

        os.system(
            "shutdown /r /t 1"
        )

        return message

    # ---------- CANCEL SHUTDOWN ----------

    if "cancel shutdown" in c:

        os.system(
            "shutdown /a"
        )

        message = "Shutdown cancelled"

        speak(message)

        return message
    # ---------- TASK MANAGER ----------

    if (
    "task manager" in c
    or "open task manager" in c):
        message = "Opening Task Manager"

        speak(message)

        os.system("start taskmgr")

        return message


    # ---------- SETTINGS ----------

    if (
    "settings" in c
    or "open settings" in c):

        message = "Opening Settings"

        speak(message)

        os.system("start ms-settings:")

        return message


    # ---------- CONTROL PANEL ----------

    if (
    "control panel" in c
    or "open control panel" in c):

        message = "Opening Control Panel"

        speak(message)

        os.system("control")

        return message
    
    if "open downloads" in c:

        path = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        os.startfile(path)

        return "Opening Downloads folder"
    
    if "open documents" in c:

        path = os.path.join(
            os.path.expanduser("~"),
            "Documents"
        )

        os.startfile(path)

        return "Opening Documents folder"

    # ---------- BATTERY ----------

    if (
        "battery percentage" in c
        or "battery status" in c
        or c == "battery"
    ):

        result = get_battery()

        speak(result)

        return result

    # ---------- CPU ----------

    if (
        "cpu usage" in c
        or "cpu status" in c
    ):

        result = get_cpu()

        speak(result)

        return result

    # ---------- RAM ----------

    if (
        "ram usage" in c
        or "memory usage" in c
    ):

        result = get_ram()

        speak(result)

        return result

    # ---------- SYSTEM STATUS ----------

    if (
        "system status" in c
        or "computer status" in c
    ):

        result = get_system_status()

        speak(result)

        return result

    return False
