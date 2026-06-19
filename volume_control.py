import pyautogui

from pycaw.pycaw import AudioUtilities
from pycaw.pycaw import IAudioEndpointVolume

from comtypes import CLSCTX_ALL


def volume_up():

    pyautogui.press(
        "volumeup"
    )


def volume_down():

    pyautogui.press(
        "volumedown"
    )


def mute():

    pyautogui.press(
        "volumemute"
    )


def unmute():

    pyautogui.press(
        "volumemute"
    )


def set_volume(percent):

    try:

        percent = max(
            0,
            min(percent, 100)
        )

        devices = (
            AudioUtilities.GetSpeakers()
        )

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        volume = interface.QueryInterface(
            IAudioEndpointVolume
        )

        volume.SetMasterVolumeLevelScalar(
            percent / 100.0,
            None
        )

        return True

    except Exception as e:

        print(
            "Volume Error:",
            e
        )

        return False