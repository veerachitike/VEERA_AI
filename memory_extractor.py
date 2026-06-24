import re

def extract_memory(text):

    patterns = [
        (
            r"my favorite (.+?) is (.+)",
            "favorite_{}"
        ),
        (
            r"my name is (.+)",
            "name"
        )
    ]

    for pattern, key_template in patterns:

        match = re.search(
            pattern,
            text.lower()
        )

        if match:

            if "{}" in key_template:

                key = key_template.format(
                    match.group(1).replace(
                        " ",
                        "_"
                    )
                )

                value = match.group(2)

            else:

                key = key_template
                value = match.group(1)

            return key, value

    return None