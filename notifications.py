class Notifications:
    def __init__(self):
        self.reminders = []

    def add_reminder(self, message):
        self.reminders.append(message)

    def get_reminders(self):
        return self.reminders