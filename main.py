import os
from datetime import datetime
import time
import speech_recognition as sr
import json
from commands import processcommand
from config import WAKE_WORDS, ACTIVE_TIMEOUT
from speech import speak
import commands
from notifications import notify
print(commands.__file__)
VERSION = "1.6"
CHAT_MODE = False

print("=" * 40)
print(f"     VEERA AI v{VERSION}")
print("=" * 40)

print(f"Wake Words: {WAKE_WORDS}")
print(f"Chat Mode: {CHAT_MODE}")

def startup_check():


    speak("Initializing VEERA")

    print("Checking folders...")

    os.makedirs("Screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    print("Folders OK")

    speak("System ready")
    notify(
    "VEERA AI",
    "System Initializing"
    )
startup_check()

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Calibrating microphone...")

    r.adjust_for_ambient_noise(
    source,
    duration=2
)

def voice_enabled():

    try:

        with open(
            "settings.json",
            "r",
            encoding="utf-8"
        ) as f:

            settings = json.load(f)

        return settings.get(
            "voiceEnabled",
            True
        )

    except Exception as e:

        print(
            "Settings Read Error:",
            e
        )

        return True
if __name__ == "__main__":

    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.2
    while True:
        if not voice_enabled():
            print(
                "Voice Assistant Disabled"
            )
            time.sleep(2)
            continue

        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = r.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=5
                )
            word = r.recognize_google(audio)
            print("HEARD:", word)
            with open(
                "logs/wakeword.log",
                "a",
                encoding="utf-8"
            ) as f:
                f.write(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {word}\n"
                )
            heard = word.lower().strip()
            wake_detected = any(
                wake.lower() == heard
                or wake.lower() in heard
                for wake in WAKE_WORDS
            )
            if wake_detected:
                speak("Yes, I am listening")
                print("ACTIVE MODE STARTED")
                miss_count = 0
                while True:
                    try:
                        with sr.Microphone() as source:
                            print("ACTIVE MODE...")
                            audio = r.listen(
                                source,
                                timeout=ACTIVE_TIMEOUT,
                                phrase_time_limit=10
                            )
                        command = r.recognize_google(audio)
                        miss_count = 0
                        print("COMMAND:", command)
                        with open(
                            "logs/commands.log",
                            "a",
                            encoding="utf-8"
                        ) as f:
                            f.write(
                                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {command}\n"
                            )
                        command_lower = command.lower()
                        if (
                            "start chat mode" in command_lower
                            or "activate chat mode" in command_lower
                            or "enable chat mode" in command_lower
                        ):
                            CHAT_MODE = True
                            speak("Chat mode activated")
                            print("CHAT MODE: ON")
                            continue
                        if (
                            "exit chat mode" in command_lower
                            or "disable chat mode" in command_lower
                            or "stop chat mode" in command_lower
                        ):
                            CHAT_MODE = False
                            speak("Chat mode deactivated")
                            print("CHAT MODE: OFF")
                            continue
                        if (
                            "sleep" in command_lower
                            or "stop listening" in command_lower
                        ):
                            speak("Going to sleep")
                            break
                        if (
                            command_lower.strip() == "shutdown veera"
                            or command_lower.strip() == "shut down veera"
                        ):
                            speak("Shutting down")
                            raise SystemExit
                        processcommand(command)
                    except sr.UnknownValueError:

                        miss_count += 1

                        if not CHAT_MODE:

                            print(
                                f"Didn't catch that ({miss_count}/5)"
                            )

                            if miss_count >= 5:

                                speak("Going to sleep")

                                break
                    except SystemExit:
                        raise
                    except Exception as e:
                        print(
                            f"[ACTIVE MODE ERROR] {type(e).__name__}: {e}"
                        )
        except sr.UnknownValueError:
            pass
        except sr.WaitTimeoutError:
            pass
        except SystemExit:
            raise
        except KeyboardInterrupt:
            print("\nVEERA stopped by user")

            speak("Goodbye")

            break

        except Exception as e:

            print(
                f"[MAIN LOOP ERROR] {type(e).__name__}: {e}"
            )

