from django.urls import path
from rest_framework.routers import SimpleRouter

from tasks.apps import TasksConfig
from tasks.views import EmployeeViewSet, TaskCreateAPIView, EmployeeBusyListView

app_name = TasksConfig.name

router = SimpleRouter()
router.register('employees', EmployeeViewSet)

urlpatterns = [path('create/', TaskCreateAPIView.as_view(), name='task-create'),
               path("employees/busy/", EmployeeBusyListView.as_view(), name='employee-busy'),

               ] + router.urls
