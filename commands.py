from memory_commands import handle_memory
from web_commands import handle_web
from media_commands import handle_media
from system_commands import handle_system
from app_commands import handle_apps
from utility_commands import handle_utility
from ai_commands import handle_ai
from help_commands import handle_help
from screenshot_commands import handle_screenshot
from clipboard_commands import handle_clipboard
from logger import log_command
from history_commands import handle_history
from command_utils import normalize_command
from dashboard_commands import handle_dashboard
print("COMMANDS FILE LOADED")


def processcommand(c):

    print("Received:", c)

    c = normalize_command(c)

    # ---------- CLIPBOARD ----------

    result = handle_clipboard(c)
    if result:
        log_command(c, result)
        return result
    
    result = handle_history(c)

    if result:
        log_command(c, result)
        return result
    # ---------- SYSTEM ----------

    result = handle_system(c)
    if result:
        log_command(c, result)
        return result
    result = handle_dashboard(c)

    if result:
        log_command(c, result)
        return result
    # ---------- HELP ----------

    result = handle_help(c)
    if result:
        log_command(c, result)
        return result

    # ---------- MEMORY ----------

    result = handle_memory(c)
    if result:
        log_command(c, result)
        return result

    # ---------- APPS ----------

    result = handle_apps(c)
    if result:
        log_command(c, result)
        return result

    # ---------- SCREENSHOTS ----------

    result = handle_screenshot(c)
    if result:
        log_command(c, result)
        return result

    # ---------- WEB ----------

    result = handle_web(c)
    if result:
        log_command(c, result)
        return result

    # ---------- MEDIA ----------

    result = handle_media(c)
    if result:
        log_command(c, result)
        return result

    # ---------- UTILITIES ----------

    result = handle_utility(c)
    if result:
        log_command(c, result)
        return result

    # ---------- AI FALLBACK ----------

    result = handle_ai(c)

    log_command(c, result)

    return result