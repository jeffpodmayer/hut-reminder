from django.db import models

# Hut - name, location
class Hut(models.Model):
  name = models.CharField(max_length=255, unique=True)
  
  def __str__(self):
    return self.name

# Reminder - start_date, end_date, notification type, is_active
class Reminder(models.Model):
    email = models.EmailField()
    hut = models.ForeignKey(Hut, on_delete=models.CASCADE, related_name="reminders")
    start_date = models.DateField()
    end_date = models.DateField()

    NOTIFICATION_CHOICES = [
      ('email', 'Email'), 
      ('sms', 'SMS'), 
    ]

    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
      return (f"Reminder for {self.hut.name} | Email: {self.email} | "
            f"Start: {self.start_date} | End: {self.end_date} | "
            f"Notification: {self.notification_type} | Active: {self.is_active}")


