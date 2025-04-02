from django.urls import path
from rest_framework.routers import SimpleRouter

from tasks.apps import TasksConfig
from tasks.views import EmployeeViewSet, TaskCreateAPIView, EmployeeBusyListView, TaskUrgentListAPIView, \
    TaskListAPIView, TaskUpdateAPIView

app_name = TasksConfig.name

router = SimpleRouter()
router.register('employees', EmployeeViewSet)

urlpatterns = [path('create/', TaskCreateAPIView.as_view(), name='task-create'),
               path('', TaskListAPIView.as_view(), name='tasks-list'),
               path('update/<int:pk>/', TaskUpdateAPIView.as_view(), name='task-update'),

               path('urgent/', TaskUrgentListAPIView.as_view(), name='tasks-urgent'),

               path("employees/busy/", EmployeeBusyListView.as_view(), name='employee-busy'),
               ] + router.urls
