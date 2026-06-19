import psutil


def get_battery():

    battery = psutil.sensors_battery()

    if battery is None:
        return "Battery information unavailable"

    status = (
        "charging"
        if battery.power_plugged
        else "not charging"
    )

    return (
        f"Battery is at {battery.percent}% "
        f"and is currently {status}"
    )


def get_cpu():

    cpu = psutil.cpu_percent(
        interval=0.1
    )

    return (
        f"CPU usage is {cpu}%"
    )


def get_ram():

    ram = psutil.virtual_memory()

    return (
        f"RAM usage is {ram.percent}% "
        f"({round(ram.used / (1024**3), 1)} GB used "
        f"of {round(ram.total / (1024**3), 1)} GB)"
    )


def get_disk():

    disk = psutil.disk_usage("/")

    return (
        f"Disk usage is {disk.percent}% "
        f"({round(disk.used / (1024**3), 1)} GB used "
        f"of {round(disk.total / (1024**3), 1)} GB)"
    )


def get_uptime():

    uptime_seconds = int(
        psutil.boot_time()
    )

    return uptime_seconds


def get_system_status():

    battery = psutil.sensors_battery()

    battery_text = (
        f"{battery.percent}%"
        if battery
        else "unavailable"
    )

    cpu = psutil.cpu_percent(
        interval=0.1
    )

    ram = psutil.virtual_memory()

    disk = psutil.disk_usage("/")

    return (
        f"Battery: {battery_text}. "
        f"CPU: {cpu}%. "
        f"RAM: {ram.percent}%. "
        f"Disk: {disk.percent}%."
    )