import os

MEMORY_FILE = "memory.txt"


def normalize_key(key):

    key = key.lower().strip()

    # British → American spelling
    key = key.replace(
        "favourite",
        "favorite"
    )

    # Underscores → spaces
    key = key.replace(
        "_",
        " "
    )

    # Remove leading "my"
    if key.startswith("my "):
        key = key[3:]

    return key


def load_memories():

    memories = {}

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                if "=" in line:

                    key, value = line.split(
                        "=",
                        1
                    )

                elif ":" in line:

                    key, value = line.split(
                        ":",
                        1
                    )

                elif "-" in line:

                    key, value = line.split(
                        "-",
                        1
                    )

                else:

                    continue

                memories[
                    normalize_key(key)
                ] = value.strip()

    except FileNotFoundError:

        pass

    except Exception as e:

        print(
            "Memory Load Error:",
            e
        )

    return memories


def save_memory(key, value):

    memories = load_memories()

    key = normalize_key(key)

    memories[key] = value.strip()

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

    key = normalize_key(key)

    return memories.get(key)


def list_memories():

    memories = load_memories()

    return list(
        memories.items()
    )


def search_memory(query):

    memories = load_memories()

    results = []

    query = normalize_key(query)

    for k, v in memories.items():

        if (
            query in k.lower()
            or query in v.lower()
        ):

            results.append(
                (k, v)
            )

    return results


def delete_memory(key):

    memories = load_memories()

    key = normalize_key(key)

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

        print(
            f"DELETED -> {key}"
        )

        return True

    except Exception as e:

        print(
            "Memory Delete Error:",
            e
        )

        return False