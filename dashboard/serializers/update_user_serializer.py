from rest_framework import serializers

from dashboard.models import User
from mvp_task import errors


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'role')

    def validate(self, attrs):
        try:
            request = self.context['request']
            user = request.user
            username = attrs['username']
            if username != user.username:
                User.objects.get(username=username)
                raise serializers.ValidationError(
                    errors.DUPLICATE_USERNAME_ERROR
                )
        except User.DoesNotExist:
            pass
        return attrs
