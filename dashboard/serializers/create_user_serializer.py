from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from dashboard.models import User
from mvp_task import errors


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'role')

    def validate(self, attrs):
        try:
            validate_password(attrs['password'])
            User.objects.get(username=attrs['username'])
            raise serializers.ValidationError(
                errors.DUPLICATE_USERNAME_ERROR
            )
        except User.DoesNotExist:
            pass
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        self.instance = User(username=data['username'], role=data['role'])
        self.instance.set_password(data['password'])
        self.instance.save()
        return self.instance
