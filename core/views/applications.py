from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from core.serializers import JobApplicationSerializer
from core.permissions import IsOwnerOrAdmin
from core.utils.pagination import CachedPagination
from core.repositories.applications import JobApplicationRepository


class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = CachedPagination

    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.query_params.get("status")
        return JobApplicationRepository.get_all(user, status_filter)

    def perform_create(self, serializer):
        JobApplicationRepository.create(applicant=self.request.user, **serializer.validated_data)

    def perform_update(self, serializer):
        application = self.get_object()
        JobApplicationRepository.update(application, **serializer.validated_data)

    def perform_destroy(self, instance):
        JobApplicationRepository.delete(instance)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def accept(self, request, pk=None):
        application = self.get_object()
        if not getattr(request.user, "is_employer", False):
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        JobApplicationRepository.accept(application)
        return Response({"status": "accepted"})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        application = self.get_object()
        if not getattr(request.user, "is_employer", False):
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        JobApplicationRepository.reject(application)
        return Response({"status": "rejected"})

    @action(detail=False, methods=['get'], url_path='by-job/(?P<job_id>[^/.]+)')
    def by_job(self, request, job_id=None):
        user = request.user
        if not getattr(user, "is_employer", False):
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        status_filter = request.query_params.get("status")
        qs = JobApplicationRepository.get_by_job(user, job_id, status_filter)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
