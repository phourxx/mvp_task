from rest_framework import serializers

from dashboard.models import User
from mvp_task.constants import ROLES


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'deposit', 'role', 'date_joined', 'updatedAt')

    def get_role(self, obj: User) -> str:
        return ROLES.get(obj.role)
