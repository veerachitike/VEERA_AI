from memory import (
    save_memory,
    get_memory,
    search_memory,
    list_memories,
    delete_memory
)

from speech import speak
import json
from notifications import notify
def handle_memory(c):

    c = c.lower().strip()

    # ---------- SAVE MEMORY ----------

    if c.startswith("remember"):

        try:

            text = c.replace(
                "remember that",
                ""
            ).replace(
                "remember",
                ""
            ).strip()

            key, value = text.split(
                " is ",
                1
            )

            with open(
                "settings.json",
                "r",
                encoding="utf-8"
            ) as f:

                settings = json.load(f)

            if not settings.get(
                "memoryEnabled",
                True
            ):

                message = (
                    "Memory system is disabled"
                )

                speak(message)

                return message

            save_memory(
                key,
                value.strip()
            )
            notify(
                "VEERA Memory",
                f"Saved: {key}"
            )
            message = (
                f"Memory saved: {key} = {value}"
            )

            speak(
                "I will remember that"
            )

            return message

        except Exception:

            message = (
                "Please use: remember something is something"
            )

            speak(message)

            return message

    # ---------- RECALL MEMORY ----------

    if c.startswith("what is"):

        key = c.replace(
            "what is",
            ""
        ).strip()

        value = get_memory(key)

        if value:

            message = (
                f"Your {key} is {value}"
            )

            speak(message)

            return message

        return False

    # ---------- FORGET MEMORY ----------

    if c.startswith("forget"):

        key = c.replace(
            "forget",
            ""
        ).strip()

        success = delete_memory(key)

        if success:

            message = (
                f"I forgot {key}"
            )

        else:

            message = (
                f"I do not know {key}"
            )

        speak(message)

        return message

    # ---------- SEARCH MEMORY ----------

    if c.startswith("search memory"):

        query = c.replace(
            "search memory",
            ""
        ).strip()

        results = search_memory(
            query
        )

        if not results:

            message = (
                "No matching memories found"
            )

            speak(message)

            return message

        response = (
            "I found these memories:\n\n"
        )

        for key, value in results:

            response += (
                f"• {key}: {value}\n"
            )

        speak(
            "I found matching memories"
        )

        return response

    # ---------- WHO AM I ----------

    if "who am i" in c:

        value = get_memory(
            "name"
        )

        if value:

            message = (
                f"You are {value}"
            )

        else:

            message = (
                "I do not know your name yet"
            )

        speak(message)

        return message

    # ---------- LIST MEMORIES ----------

    if (
        "what do you know about me" in c
        or "what do you remember" in c
        or "show memories" in c
        or "list memories" in c
    ):

        memories = list_memories()

        if not memories:

            message = (
                "I do not know anything about you yet"
            )

            speak(message)

            return message

        response = (
            "I know the following about you:\n\n"
        )

        for key, value in memories:

            response += (
                f"• {key}: {value}\n"
            )

        speak(
            "Here is what I know about you"
        )

        return response

    return False