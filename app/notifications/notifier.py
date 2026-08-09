from plyer import notification


class Notifier:

    def send(self, title: str, message: str):

        notification.notify(
            title=title,
            message=message,
            app_name="Placement Agent",
            timeout=60,
        )