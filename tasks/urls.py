from rest_framework.routers import SimpleRouter

from tasks.apps import TasksConfig
from tasks.views import EmployeeViewSet

app_name = TasksConfig.name

router = SimpleRouter()
router.register('employees', EmployeeViewSet)

urlpatterns = [

] + router.urls
