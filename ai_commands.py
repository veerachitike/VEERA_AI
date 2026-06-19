from ai import ask_ai
from speech import speak


def handle_ai(c):

    try:

        response = ask_ai(c)

        if not response:

            message = (
                "I could not generate a response."
            )

            speak(message)

            return message

    except Exception as e:

        print(
            "AI Error:",
            e
        )

        message = (
            "I am unable to contact the AI service."
        )

        speak(message)

        return message

    print("\nAI RESPONSE:")
    print(response)

    # Clean response for TTS
    short_response = (
        response
        .replace("*", "")
        .replace("#", "")
        .replace("\n", " ")
    )

    try:

        speak(
            short_response[:300]
        )

    except Exception as e:

        print(
            "Speech Error:",
            e
        )

    # IMPORTANT:
    # Return actual Gemini response
    return response.strip()