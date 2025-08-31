from rest_framework import serializers
from core.models import Job


class JobSerializer(serializers.ModelSerializer):
    employer_name = serializers.ReadOnlyField(source='employer.username')

    class Meta:
        model = Job
        fields = ['id', 'employer', 'employer_name', 'title', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['employer', 'status', 'created_at', 'updated_at']
