from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import Job
from core.serializers import JobSerializer
from core.permissions import IsEmployer, IsOwnerOrAdmin


class JobViewSet(viewsets.ModelViewSet):

    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Job.objects.all()
        elif user.is_employer:
            return Job.objects.filter(employer=user)
        else:  # job seeker
            return Job.objects.filter(status='approved', is_published=True)

    def perform_create(self, serializer):
        # Job is created by employer, starts as pending
        serializer.save(employer=self.request.user, status='pending')

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):

        job = self.get_object()
        if not request.user.is_staff:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        job.status = 'approved'
        job.save()
        return Response({"status": "approved"})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):

        job = self.get_object()
        if not request.user.is_staff:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        reason = request.data.get("reason", "")
        job.status = 'rejected'
        job.rejection_reason = reason
        job.save()
        return Response({"status": "rejected", "reason": reason})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):

        job = self.get_object()
        if not request.user.is_staff:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        if job.status != 'approved':
            return Response({"detail": "Job must be approved first"}, status=status.HTTP_400_BAD_REQUEST)
        job.is_published = True
        job.save()
        return Response({"status": "published"})
