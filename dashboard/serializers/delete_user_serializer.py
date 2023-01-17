from django.contrib.auth import authenticate
from rest_framework import serializers

from dashboard.models import User
from mvp_task import errors


class DeleteUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('password', )

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        password = attrs['password']
        auth = authenticate(request=self.context['request'],
                            username=user.username, password=password)
        if auth is None:
            raise serializers.ValidationError(
                errors.INCORRECT_PASSWORD_ERROR
            )
        return attrs
