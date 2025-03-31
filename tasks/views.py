from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tasks.models import Employee
from tasks.serializers import EmployeeSerializer, EmployeeDetailSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return EmployeeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
