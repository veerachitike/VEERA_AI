def normalize_command(c):

    c = c.lower().strip()

    replacements = {
        "clip board": "clipboard",
        "task manager": "taskmanager",
        "shut down": "shutdown",
        "re start": "restart",
        "web site": "website",
    }

    for old, new in replacements.items():

        c = c.replace(
            old,
            new
        )

    return c