import asyncio
import edge_tts
import pygame
import os
import tempfile
import threading


VOICE = "en-US-JennyNeural"


# Initialize once
try:

    if not pygame.mixer.get_init():

        pygame.mixer.init(
            frequency=44100
        )

except Exception as e:

    print(
        "Audio Init Error:",
        e
    )


async def _speak(text):

    temp_file = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ) as temp:

            temp_file = temp.name

        communicate = edge_tts.Communicate(
            text,
            voice=VOICE
        )

        await communicate.save(
            temp_file
        )

        pygame.mixer.music.load(
            temp_file
        )

        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():

            await asyncio.sleep(0.1)

        pygame.mixer.music.unload()

    except Exception as e:

        print(
            "Edge TTS Error:",
            e
        )

        raise

    finally:

        if (
            temp_file
            and os.path.exists(temp_file)
        ):

            try:

                os.remove(temp_file)

            except Exception as e:

                print(
                    "File Delete Error:",
                    e
                )


def _fallback_speak(text):

    try:

        import pyttsx3

        engine = pyttsx3.init()

        voices = engine.getProperty(
            "voices"
        )

        if len(voices) > 1:

            engine.setProperty(
                "voice",
                voices[1].id
            )

        engine.setProperty(
            "rate",
            170
        )

        engine.say(text)

        engine.runAndWait()

    except Exception as e:

        print(
            "Fallback TTS Error:",
            e
        )


def _run_speech(text):

    try:

        asyncio.run(
            _speak(text)
        )

    except Exception as e:

        print(
            "TTS Error:",
            e
        )

        print(
            "Using fallback voice"
        )

        _fallback_speak(text)


def speak(text):

    print(
        f"VEERA: {text}"
    )

    # Run speech in background
    threading.Thread(
        target=_run_speech,
        args=(text,),
        daemon=True
    ).start()


if __name__ == "__main__":

    speak(
        "Testing voice"
    )

    input(
        "Press Enter to exit..."
    )