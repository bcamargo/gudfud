from rest_framework import serializers
from foodie.models import BaseUser


class BaseUserSerializer(serializers.ModelSerializer):
    """
    User Registration Serializer
    """

    def validate_email(self, value):
        """
        Check if the email is not registered by another user
        """
        email_exists = BaseUser.objects.filter(email=value).exists()
        if email_exists:
            raise serializers.ValidationError("Email already registered by another user.")
        else:
            return value

    def validate_password(self, value):
        """
        Validate password
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        else:
            return value

    def create(self, validated_data):
        base_user = BaseUser(**validated_data)
        base_user.is_active = True
        base_user.set_password(base_user.password)
        base_user.save()
        return base_user

    class Meta:
        model = BaseUser