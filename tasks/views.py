from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from tasks.models import Employee, Task
from tasks.serializers import EmployeeSerializer, EmployeeDetailSerializer, TaskSerializer, EmployeeBusySerializer


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
    permission_classes = (IsAuthenticated,)


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
