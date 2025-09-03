from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import JobApplication, Notification
from core.tasks import send_notification_email


@receiver(post_save, sender=JobApplication)
def job_applied_notification(sender, instance, created, **kwargs):
    if created:
        job = instance.job
        applicant = instance.applicant
        employer = job.employer

        message = f"{applicant.username} has applied to your job: {job.title}"
        Notification.objects.create(
            user=employer,
            event='job_applied',
            job=job,
            application=instance,
            message=message
        )

        send_notification_email.delay(
            subject=f"New Application for {job.title}",
            message=message,
            recipient_list=[employer.email]
        )


@receiver(post_save, sender=JobApplication)
def application_status_notification(sender, instance, **kwargs):
    if not instance._state.adding:
        applicant = instance.applicant
        job = instance.job
        if instance.status == 'accepted':
            message = f"Your application for {job.title} has been accepted!"
            event = 'application_accepted'
        elif instance.status == 'rejected':
            message = f"Your application for {job.title} has been rejected."
            event = 'application_rejected'
        else:
            return

        Notification.objects.create(
            user=applicant,
            event=event,
            job=job,
            application=instance,
            message=message
        )

        send_notification_email.delay(
            subject=f"Application Update for {job.title}",
            message=message,
            recipient_list=[applicant.email]
        )
