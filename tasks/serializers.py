from rest_framework import serializers

from tasks.models import Employee, Task
from tasks.services import get_least_busy_employee


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "deadline", "status", "executor", "parental_task"]


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "deadline", "status", "executor", "parental_task", "attachment",
                  "comment"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeBusySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    active_tasks = serializers.SerializerMethodField()

    def get_active_tasks(self, obj):
        return obj.tasks.filter(status='started').count()

    class Meta:
        model = Employee
        fields = ["id", "fullname", "department", "role", "user", "active_tasks", "tasks"]


class EmployeeDetailSerializer(serializers.ModelSerializer):
    crew = serializers.SerializerMethodField()

    def get_crew(self, obj):
        user = self.context.get("request").user
        if obj.is_supervisor:
            crew_members = Employee.objects.filter(department=obj.department).exclude(user=user.id)
            return EmployeeSerializer(crew_members, many=True).data
        return []

    class Meta:
        model = Employee
        fields = ["id", "fullname", "department", "role", "user", "crew"]


class UrgentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "deadline"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        executor = get_least_busy_employee(instance.parental_task.pk)
        if executor:
            representation['candidate'] = [executor.fullname]
        else:
            representation['candidate'] = "Нет свободных сотрудников"
        return representation
