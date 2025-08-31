from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import JobApplicationViewSet

router = DefaultRouter()
router.register(r'applications', JobApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]
