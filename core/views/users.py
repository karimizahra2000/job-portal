from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken

from core.serializers import RegisterSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from core.tasks import send_verification_email, send_password_reset_email
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relative_link = reverse("verify-email")
            link = f"http://{current_site}{relative_link}?token={str(token)}"

            send_verification_email.delay(user.email, link)

            return Response({"message": "Check your email to verify your account."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get("token")
        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.is_verified = True
            user.save()

            if user.is_seeker:
                from core.models import JobSeekerProfile
                JobSeekerProfile.objects.get_or_create(user=user)
            elif user.is_employer:
                from core.models import EmployerProfile
                EmployerProfile.objects.get_or_create(user=user)

            return Response({"message": "Email verified successfully. You can now log in."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            token = str(AccessToken.for_user(user))
            reset_link = f"http://localhost:8000/api/users/password-reset/confirm/?token={token}"

            send_password_reset_email.delay(user.email, reset_link)

            return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']

        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = User.objects.get(id=user_id)
            user.set_password(password)
            user.save()

            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)