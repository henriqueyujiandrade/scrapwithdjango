from rest_framework import serializers

from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=127)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    birthdate = serializers.DateField()
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        user_obj = User.objects.create_user(**validated_data)

        return user_obj

    def validate_email(self, value):
        email_exists = User.objects.filter(email__iexact=value).exists()

        if email_exists:
            raise serializers.ValidationError("email already exists")

        return value

    def validate_username(self, value):
        username_exists = User.objects.filter(username__iexact=value).exists()

        if username_exists:
            raise serializers.ValidationError("username already exists")

        return value


class PatchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "birthdate",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
        ]
        read_only_fields = ["date_joined", "is_active", "is_staff", "is_superuser"]


class DeleteOrChangeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "birthdate",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
        ]
        read_only_fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "birthdate",
            "date_joined",
            "is_superuser",
        ]