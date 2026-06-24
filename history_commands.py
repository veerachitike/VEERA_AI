from speech import speak

LOG_FILE = "logs/commands.log"


def handle_history(c):

    c = c.lower().strip()

    if (
        "show history" in c
        or "command history" in c
        or "recent commands" in c
        or "last commands" in c
    ):

        try:

            with open(
                LOG_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                lines = file.readlines()

            if not lines:

                message = (
                    "No command history found"
                )

                speak(message)

                return message

            recent = lines[-10:]

            response = (
                "Recent Commands:\n\n"
            )

            for line in recent:

                response += line

            speak(
                "Showing recent commands"
            )

            return response

        except Exception as e:

            print(
                "History Error:",
                e
            )

            return (
                "Unable to load command history"
            )

    return False