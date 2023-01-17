from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from mvp_task import errors


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8,
                                     max_length=16)
    user = None

    def validate(self, attrs):
        user = authenticate(request=self.context['request'], **attrs)
        if user:
            try:
                Token.objects.get(user=user)
                raise serializers.ValidationError(errors.ACTIVE_SESSION_ERROR)
            except Token.DoesNotExist:
                self.user = user
        else:
            raise serializers.ValidationError(errors.INVALID_LOGIN_ERROR)
        return attrs
