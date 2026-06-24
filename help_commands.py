from speech import speak


def handle_help(c):

    if (
        c == "help"
        or "what can you do" in c
        or "show commands" in c
        or "show help" in c
    ):

        response = """
VEERA COMMANDS

APPLICATIONS
• Open Chrome
• Open Edge
• Open VS Code
• Open Spotify
• Close Apps

SYSTEM
• Battery Status
• CPU Usage
• RAM Usage
• System Status
• Open Task Manager
• Open Settings
• Open Downloads

MEMORY
• Remember ...
• What is ...
• Forget ...
• Search Memory ...
• List Memories

WEB
• Search ...
• Open Website ...
• Weather ...

MEDIA
• Play Music
• Open YouTube
"""

        speak(
            "Showing available commands"
        )

        return response

    return False