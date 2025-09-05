from core.models import Job
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet


class JobRepository:
    @staticmethod
    def get_all(user, status_filter: str | None = None) -> QuerySet:

        if user.is_staff:
            qs = Job.objects.all()
        elif getattr(user, "is_employer", False):
            qs = Job.objects.filter(employer=user)
        else:  # job seeker
            qs = Job.objects.filter(status='approved', is_published=True)

        if status_filter:
            qs = qs.filter(status=status_filter)

        return qs.order_by("-created_at")

    @staticmethod
    def get_by_id(job_id: int) -> Job:
        return get_object_or_404(Job, id=job_id)

    @staticmethod
    def create(employer, **kwargs) -> Job:

        return Job.objects.create(employer=employer, status='pending', **kwargs)

    @staticmethod
    def update(job: Job, **kwargs) -> Job:
        for field, value in kwargs.items():
            setattr(job, field, value)
        job.save()
        return job

    @staticmethod
    def delete(job: Job):
        job.delete()

    @staticmethod
    def approve(job: Job):
        job.status = 'approved'
        job.save()
        return job

    @staticmethod
    def reject(job: Job, reason: str = ""):
        job.status = 'rejected'
        job.rejection_reason = reason
        job.save()
        return job

    @staticmethod
    def publish(job: Job):
        if job.status != 'approved':
            raise ValueError("Job must be approved first")
        job.is_published = True
        job.save()
        return job
