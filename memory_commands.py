from memory import (
    save_memory,
    get_memory,
    list_memories
)

from speech import speak


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

            ALIASES = {
                "my name": "name",
                "my favourite language": "favorite language",
                "my favorite language": "favorite language"
            }

            key = ALIASES.get(
                key.strip().lower(),
                key.strip().lower()
            )

            value = value.strip()

            save_memory(
                key,
                value
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
                "Please use: remember that something is something"
            )

            speak(message)

            return message

    # ---------- RECALL MEMORY ----------

    if c.startswith("what is"):

        key = c.replace(
            "what is",
            ""
        ).strip()

        ALIASES = {
            "my name": "name",
            "my favorite language": "favorite language",
            "my favourite language": "favorite language"
        }

        key = ALIASES.get(
            key,
            key
        )

        value = get_memory(key)

        if value:

            message = (
                f"Your {key} is {value}"
            )

            speak(message)

            return message

        message = (
            f"I do not know your {key} yet"
        )

        speak(message)

        return message

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

    if "what do you know about me" in c:

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