from rest_framework import serializers

from tasks.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeDetailSerializer(serializers.ModelSerializer):
    crew = serializers.SerializerMethodField()

    def get_crew(self, obj):
        user = self.context.get("request").user
        if obj.is_supervisor:
            crew_members = Employee.objects.filter(position=obj.position).exclude(user=user.id)
            return EmployeeSerializer(crew_members, many=True).data
        return []

    class Meta:
        model = Employee
        fields = ["id", "fullname", "position", "user", "crew"]
