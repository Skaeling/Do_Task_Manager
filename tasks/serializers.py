from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from tasks.models import Employee, Task
from tasks.services import get_least_busy_employee
from tasks.validators import validate_deadline, WordsValidator, validate_executor_tasks, validate_attachment_size


class TaskSerializer(serializers.ModelSerializer):
    """Для просмотра списка всех задач"""

    class Meta:
        model = Task
        fields = ["id", "title", "deadline", "status", "executor", "parental_task"]


class TaskDetailSerializer(serializers.ModelSerializer):
    """Для создания и обновления задачи"""
    deadline = serializers.DateTimeField(validators=[validate_deadline])
    executor = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(),
                                                  validators=[validate_executor_tasks], required=False)
    attachment = serializers.FileField(validators=[
        validate_attachment_size,
        FileExtensionValidator(allowed_extensions=['png', 'jpg', 'doc'],
                               message="Расширение файла “%(extension)s” недопустимо. "
                                       "Выберите файл типа: %(allowed_extensions)s.")], required=False)

    validators = [WordsValidator('title', 'description', 'comment')]

    class Meta:
        model = Task
        fields = ["id", "title", "description", "deadline", "status", "executor", "parental_task", "attachment",
                  "comment"]


class UrgentTaskSerializer(serializers.ModelSerializer):
    """Для просмотра важных задач и свободных кандидатов"""

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


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeBusySerializer(serializers.ModelSerializer):
    """Для просмотра списка сотрудников по количеству активных задач"""

    tasks = TaskSerializer(many=True, read_only=True)
    active_tasks = serializers.IntegerField(source='active_tasks_count', read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "fullname", "department", "role", "active_tasks", "tasks"]


class EmployeeDetailSerializer(serializers.ModelSerializer):
    crew = serializers.SerializerMethodField()

    def get_crew(self, obj):
        user = self.context.get("request").user
        if obj.is_supervisor:
            crew_members = Employee.objects.filter(department=obj.department).exclude(user=user.id)
            return EmployeeSerializer(crew_members, many=True).data
        return None

    class Meta:
        model = Employee
        fields = ["id", "fullname", "department", "role", "user", "crew"]
