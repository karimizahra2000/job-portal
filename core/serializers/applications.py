from rest_framework import serializers
from core.models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.ReadOnlyField(source='applicant.username')
    job_title = serializers.ReadOnlyField(source='job.title')

    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'job_title', 'applicant', 'applicant_name',
            'cover_letter', 'resume', 'status', 'applied_at'
        ]
        read_only_fields = ['applicant', 'status', 'applied_at']
