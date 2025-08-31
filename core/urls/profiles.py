from django.urls import path
from core.views import JobSeekerProfileView, EmployerProfileView

urlpatterns = [
    path("jobseeker/", JobSeekerProfileView.as_view(), name='jobseeker-profile'),
    path("employer/", EmployerProfileView.as_view(), name='employer-profile'),
]