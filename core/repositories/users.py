from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

User = get_user_model()


class UserRepository:
    @staticmethod
    def create_user(**validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.get(id=user_id)

    @staticmethod
    def get_user_by_email(email):
        return User.objects.get(email=email)

    @staticmethod
    def activate_and_verify_user(user):
        user.is_active = True
        user.is_verified = True
        user.save()
        return user

    @staticmethod
    def set_user_password(user, password):
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def generate_access_token(user):
        return AccessToken.for_user(user)

    @staticmethod
    def generate_refresh_token(user):
        return RefreshToken.for_user(user)
