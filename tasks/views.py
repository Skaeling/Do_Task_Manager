from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from tasks.models import Employee, Task
from tasks.serializers import EmployeeSerializer, EmployeeDetailSerializer, TaskSerializer, EmployeeBusySerializer, \
    UrgentTaskSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return EmployeeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmployeeBusyListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeBusySerializer


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdateAPIView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_update(self, serializer):
        """При добавлении в задачу исполнителя меняет статус задачи с created на started"""
        task = serializer.save()
        if task.executor and task.status == 'created':
            task.status = 'started'
        task.save()


class TaskUrgentListAPIView(generics.ListAPIView):
    serializer_class = UrgentTaskSerializer

    def get_queryset(self):
        return Task.objects.filter(executor=None, parental_task__status='started')
