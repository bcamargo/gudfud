from rest_framework import serializers
from rest_framework.reverse import reverse
from foodie.models import BaseUser, Customer, Operator, Menu, MenuItem


class CustomHyperlinkedImageField(serializers.ImageField):
    def to_native(self, value):
        request = self.context.get('request', None)
        try:
            return request.build_absolute_uri(value.url)
        except ValueError:
            return ''


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


class BaseUserSerializerMixin(serializers.HyperlinkedModelSerializer):
    """
    Base user serializer mixin for use in physician and assistant serializers
    """
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    image = CustomHyperlinkedImageField(read_only=True)
    thumbnail = CustomHyperlinkedImageField(read_only=True)
    date_joined = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()


class CustomerSerializer(BaseUserSerializerMixin):
    uri = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()

    def get_uri(self, obj):
        return reverse('user-profile', request=self.context.get('request'))

    def get_user_type(self, obj):
        return 'customer'

    class Meta:
        model = Customer
        exclude = ('base_user', )


class OperatorSerializer(BaseUserSerializerMixin):
    user_type = serializers.SerializerMethodField()

    def get_user_type(self, obj):
        return 'operator'

    class Meta:
        model = Operator


class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = MenuItem


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Menu