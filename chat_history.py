import json
import os
from datetime import datetime

HISTORY_FILE = "data/chat_history.json"


def save_chat(conversation_id, user, response):

    try:

        os.makedirs(
            os.path.dirname(HISTORY_FILE),
            exist_ok=True
        )

        if os.path.exists(HISTORY_FILE):

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                try:

                    history = json.load(f)

                except json.JSONDecodeError:

                    history = {}

        else:

            history = {}

        # Convert old history format to new format
        if isinstance(history, list):

            history = {}

        history.setdefault(
            conversation_id,
            []
        )

        history[conversation_id].append({

            "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "user":
            user,

            "response":
            response

        })

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                history,
                f,
                indent=4,
                ensure_ascii=False
            )

    except Exception as e:

        print(
            "Chat Save Error:",
            e
        )


def get_history(conversation_id):

    try:

        if not os.path.exists(HISTORY_FILE):

            return []

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            history = json.load(f)

        if isinstance(history, list):

            return []

        return history.get(
            conversation_id,
            []
        )

    except Exception as e:

        print(
            "History Read Error:",
            e
        )

        return []