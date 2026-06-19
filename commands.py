from memory_commands import handle_memory
from web_commands import handle_web
from media_commands import handle_media
from system_commands import handle_system
from app_commands import handle_apps
from utility_commands import handle_utility
from ai_commands import handle_ai


def processcommand(c):

    print("Received:", c)

    c = c.lower()

    result = handle_memory(c)
    if result:
        return result

    result = handle_web(c)
    if result:
        return result

    result = handle_media(c)
    if result:
        return result

    result = handle_system(c)
    if result:
        return result

    result = handle_apps(c)
    if result:
        return result

    result = handle_utility(c)
    if result:
        return result

    return handle_ai(c)