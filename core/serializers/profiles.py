from rest_framework import serializers
from core.models import JobSeekerProfile, EmployerProfile, User


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = ['id', 'user', 'profile_picture', 'resume']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        profile = JobSeekerProfile.objects.create(user=user, **validated_data)
        return profile


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ['id', 'user', 'company_name', 'company_logo']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        profile = EmployerProfile.objects.create(user=user, **validated_data)
        return profile
