from speech import speak

from system_info import (
    get_battery,
    get_cpu,
    get_ram,
    get_system_status
)


def handle_dashboard(c):

    c = c.lower().strip()

    if (
        "dashboard" in c
        or "system dashboard" in c
        or "health check" in c
        or "system overview" in c
    ):

        battery = get_battery()
        cpu = get_cpu()
        ram = get_ram()
        status = get_system_status()

        response = f"""
VEERA SYSTEM DASHBOARD

{battery}

{cpu}

{ram}

{status}
"""

        speak(
            "Generating system dashboard"
        )

        return response.strip()

    return False