from django.db import models
from django.conf import settings


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )


class EmployerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to="company_logos/", null=True, blank=True)

    def __str__(self):
        return f"EmployerProfile - {self.company_name}"
