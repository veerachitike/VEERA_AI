from plyer import notification


def notify(title, message):

    try:

        print(
            f"NOTIFICATION -> {title}: {message}"
        )

        notification.notify(
            title=title,
            message=message,
            app_name="VEERA AI",
            timeout=5
        )

        print(
            "NOTIFICATION SENT"
        )

    except Exception as e:

        print(
            "Notification Error:",
            e
        )