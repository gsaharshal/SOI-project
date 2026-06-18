from django.db import models
from django.conf import settings
from jobs.models import Job


class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ("JOB_ALERT", "Job Alert"),
        ("APPLICATION_UPDATE", "Application Update"),
        ("SYSTEM", "System"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    notification_type = models.CharField(
    max_length=30,
    choices=NOTIFICATION_TYPES,
    default="SYSTEM"
)


    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.title}"