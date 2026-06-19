import os

MEMORY_FILE = "memory.txt"


def load_memories():

    memories = {}

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                if "=" not in line:
                    continue

                key, value = line.strip().split(
                    "=",
                    1
                )

                memories[
                    key.strip().lower()
                ] = value.strip()

    except FileNotFoundError:
        pass

    return memories


def save_memory(key, value):

    memories = load_memories()

    memories[
        key.strip().lower()
    ] = value.strip()

    try:

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            for k, v in memories.items():

                file.write(
                    f"{k}={v}\n"
                )

        print(
            f"SAVED -> {key} = {value}"
        )

        return True

    except Exception as e:

        print(
            "Memory Save Error:",
            e
        )

        return False


def get_memory(key):

    memories = load_memories()

    return memories.get(
        key.strip().lower()
    )


def list_memories():

    memories = load_memories()

    return list(
        memories.items()
    )


def delete_memory(key):

    memories = load_memories()

    key = key.strip().lower()

    if key not in memories:

        return False

    del memories[key]

    try:

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            for k, v in memories.items():

                file.write(
                    f"{k}={v}\n"
                )

        return True

    except Exception as e:

        print(
            "Memory Delete Error:",
            e
        )

        return False