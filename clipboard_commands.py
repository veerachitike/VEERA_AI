import pyperclip
from speech import speak


def handle_clipboard(c):

    c = c.lower().strip()

    # Normalize common variations

    c = c.replace(
        "clip board",
        "clipboard"
    )

    # ---------- READ CLIPBOARD ----------

    clipboard_words = [
        "clipboard"
    ]

    read_words = [
        "read",
        "show",
        "display",
        "check",
        "view",
        "what is in",
        "what's in"
    ]

    if (
        any(
            word in c
            for word in clipboard_words
        )
        and
        any(
            word in c
            for word in read_words
        )
    ):

        try:

            text = pyperclip.paste()

            if not text:

                message = (
                    "Clipboard is empty"
                )

            else:

                message = (
                    f"Clipboard contains: "
                    f"{text}"
                )

            speak(message)

            return message

        except Exception as e:

            print(
                "Clipboard Error:",
                e
            )

            return (
                "Unable to access clipboard"
            )

    # ---------- SAVE CLIPBOARD ----------

    save_words = [
        "save",
        "remember",
        "store"
    ]

    if (
        "clipboard" in c
        and
        any(
            word in c
            for word in save_words
        )
    ):

        try:

            text = pyperclip.paste()

            from memory import save_memory

            save_memory(
                "clipboard",
                text
            )

            message = (
                "Clipboard saved to memory"
            )

            speak(message)

            return message

        except Exception as e:

            print(
                "Clipboard Save Error:",
                e
            )

            return (
                "Unable to save clipboard"
            )

    return False