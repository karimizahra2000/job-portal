from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import JobApplication
from core.serializers import JobApplicationSerializer
from core.permissions import IsOwnerOrAdmin
from core.utils.pagination import CachedPagination


class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = CachedPagination

    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.query_params.get("status")  # فیلتر وضعیت اپلیکیشن

        if user.is_staff or user.is_employer:
            qs = JobApplication.objects.filter(job__employer=user)
        else:
            qs = JobApplication.objects.filter(applicant=user)

        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def accept(self, request, pk=None):
        application = self.get_object()
        if not request.user.is_employer:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        application.status = 'accepted'
        application.save()
        return Response({"status": "accepted"})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        application = self.get_object()
        if not request.user.is_employer:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        application.status = 'rejected'
        application.save()
        return Response({"status": "rejected"})

    @action(detail=False, methods=['get'], url_path='by-job/(?P<job_id>[^/.]+)')
    def by_job(self, request, job_id=None):
        user = request.user
        if not user.is_employer:
            return Response({"detail": "Not allowed"}, status=403)

        status_filter = request.query_params.get("status")
        qs = JobApplication.objects.filter(job_id=job_id, job__employer=user)

        if status_filter:
            qs = qs.filter(status=status_filter)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
