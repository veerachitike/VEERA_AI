import pywhatkit

from speech import speak

from media_control import (
    pause_music,
    resume_music,
    next_track,
    previous_track
)

from volume_control import (
    volume_up,
    volume_down,
    mute,
    unmute,
    set_volume
)


def handle_media(c):

    c = c.lower().strip()

    # ---------- PLAY MUSIC ----------

    if c.startswith("play "):

        song = c.replace(
            "play ",
            ""
        ).strip()

        try:

            speak(f"Playing {song}")

            pywhatkit.playonyt(song)

            return f"Playing {song}"

        except Exception as e:

            print("Play Error:", e)

            return f"Unable to play {song}"

    # ---------- PAUSE ----------

    if "pause music" in c:

        pause_music()

        message = "Music paused"

        speak(message)

        return message

    # ---------- RESUME ----------

    if "resume music" in c:

        resume_music()

        message = "Music resumed"

        speak(message)

        return message

    # ---------- NEXT TRACK ----------

    if "next track" in c:

        next_track()

        message = "Skipping to next track"

        speak(message)

        return message

    # ---------- PREVIOUS TRACK ----------

    if "previous track" in c:

        previous_track()

        message = "Playing previous track"

        speak(message)

        return message

    # ---------- VOLUME UP ----------

    if c == "volume up":

        volume_up()

        message = "Volume increased"

        speak(message)

        return message

    # ---------- VOLUME DOWN ----------

    if c == "volume down":

        volume_down()

        message = "Volume decreased"

        speak(message)

        return message

    # ---------- MUTE ----------

    if c == "mute":

        mute()

        message = "Audio muted"

        speak(message)

        return message

    # ---------- UNMUTE ----------

    if c == "unmute":

        unmute()

        message = "Audio unmuted"

        speak(message)

        return message

    # ---------- SET VOLUME ----------

    if (
        "set volume to" in c
        or "volume down to" in c
        or "volume up to" in c
        or c.startswith("volume ")
    ):

        try:

            level = int(
                ''.join(
                    filter(str.isdigit, c)
                )
            )

            if level < 0:
                level = 0

            if level > 100:
                level = 100

            set_volume(level)

            message = (
                f"Volume set to {level}%"
            )

            speak(message)

            return message

        except Exception:

            message = (
                "Please specify a valid volume level"
            )

            speak(message)

            return message

    return False
