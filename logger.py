import os

from datetime import datetime


LOG_FILE = "logs/commands.log"


def log_command(command, response=None):

    try:

        os.makedirs(
            "logs",
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            if response:

                file.write(
                    f"[{timestamp}] "
                    f"COMMAND: {command} | "
                    f"RESPONSE: {response}\n"
                )

            else:

                file.write(
                    f"[{timestamp}] "
                    f"COMMAND: {command}\n"
                )

    except Exception as e:

        print(
            "Logger Error:",
            e
        )