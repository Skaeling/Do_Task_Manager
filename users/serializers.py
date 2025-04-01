from rest_framework import serializers

from users.models import User
from tasks.serializers import EmployeeSerializer


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRetrieveSerializer(serializers.ModelSerializer):
    positions = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'positions']
