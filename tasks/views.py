from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from tasks.models import Employee, Task
from tasks.serializers import EmployeeSerializer, EmployeeDetailSerializer, TaskSerializer, EmployeeBusySerializer, \
    UrgentTaskSerializer, TaskDetailSerializer
from users.permissions import IsSupervisor, IsExecutor, IsOwner


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return EmployeeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = (IsSupervisor,)
        elif self.action == 'retrieve':
            self.permission_classes = (IsSupervisor | IsOwner,)
        return super().get_permissions()


class EmployeeBusyListView(generics.ListAPIView):
    """Представляет список занятых сотрудников"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeBusySerializer
    permission_classes = (IsAuthenticated, IsSupervisor)


class TaskCreateAPIView(generics.CreateAPIView):
    """Создает новую задачу"""
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = (IsAuthenticated, IsSupervisor)

    def perform_create(self, serializer):
        task = serializer.save()
        if task.executor is not None:
            task.status = "started"
            task.save()


class TaskListAPIView(generics.ListAPIView):
    """Представляет список всех задач"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRetrieveAPIView(generics.RetrieveAPIView):
    """Отображает детальную информацию о задаче,
    если она принадлежит текущему юзеру или он является супервайзером"""
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = (IsAuthenticated, IsSupervisor | IsExecutor)


class TaskUpdateAPIView(generics.UpdateAPIView):
    """"Обновляет задачу"""
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer

    def perform_update(self, serializer):
        """При добавлении в задачу исполнителя меняет статус задачи с created на started"""
        task = serializer.save()
        if task.executor and task.status == 'created':
            task.status = 'started'
        task.save()


class TaskDestroyAPIView(generics.DestroyAPIView):
    """Удаляет задачу по указанному pk"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsSupervisor)


class TaskUrgentListAPIView(generics.ListAPIView):
    """Представляет список важных задач"""
    serializer_class = UrgentTaskSerializer

    def get_queryset(self):
        return Task.objects.filter(executor=None, parental_task__status='started')
