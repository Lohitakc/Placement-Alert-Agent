from winotify import Notification


class Notifier:

    def send(self, title: str, message: str):

        toast = Notification(
            app_id="Placement Agent",
            title=title,
            msg=message
        )

        toast.show()