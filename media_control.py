import pyautogui


def pause_music():

    try:

        pyautogui.press(
            "playpause"
        )

        return True

    except Exception as e:

        print(
            "Pause Error:",
            e
        )

        return False


def resume_music():

    try:

        pyautogui.press(
            "playpause"
        )

        return True

    except Exception as e:

        print(
            "Resume Error:",
            e
        )

        return False


def next_track():

    try:

        pyautogui.press(
            "nexttrack"
        )

        return True

    except Exception as e:

        print(
            "Next Track Error:",
            e
        )

        return False


def previous_track():

    try:

        pyautogui.press(
            "prevtrack"
        )

        return True

    except Exception as e:

        print(
            "Previous Track Error:",
            e
        )

        return False