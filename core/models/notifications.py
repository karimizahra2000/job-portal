from django.db import models
from django.conf import settings
from core.models.jobs import Job
from core.models.applications import JobApplication


class Notification(models.Model):
    EVENT_CHOICES = (
        ('job_applied', 'Job Applied'),
        ('application_accepted', 'Application Accepted'),
        ('application_rejected', 'Application Rejected'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    event = models.CharField(max_length=50, choices=EVENT_CHOICES)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event} -> {self.user.username}"
