from datetime import timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import Task, Employee
from users.models import User
from django.utils import timezone


class EmployeeTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test_user@email.com", username="test_user")
        self.client.force_authenticate(user=self.user)
        self.employee = Employee.objects.create(fullname="Супервайзеров Аркадий Витальевич",
                                                user=self.user,
                                                is_supervisor=True
                                                )

    def test_employee_create(self):
        """Тестирование создания пользователя"""

        url = reverse("tasks:employee-list")
        data = {"fullname": "Тестов Тест Тестович", "user": 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.all().count(), 2)

    def test_employee_retrieve(self):
        url = reverse("tasks:employee-detail", args=(self.employee.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("fullname"), self.employee.fullname)

    def test_employee_update(self):
        url = reverse("tasks:employee-detail", args=(self.employee.pk,))
        data = {"role": "director"}
        response = self.client.patch(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("role"), data.get('role'))

    def test_employee_delete(self):
        url = reverse("tasks:employee-detail", args=(self.employee.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.all().count(), 0)

    def test_employees_list(self):
        url = reverse("tasks:employee-list")
        response = self.client.get(url)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "fullname": self.employee.fullname,
                    "role": self.employee.role,
                    "is_supervisor": self.employee.is_supervisor,
                    "department": self.employee.department,
                    "user": self.user.pk
                },
            ]
        }
        self.assertEqual(result, data)

    def test_employees_busy_list(self):
        url = reverse("tasks:employee-busy")
        response = self.client.get(url)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'count': 1,
                'next': None,
                'previous': None,
                'results': [{'active_tasks': self.employee.tasks.filter(status='started').count(),
                             'department': self.employee.department,
                             'fullname': self.employee.fullname,
                             'id': self.employee.pk,
                             'role': self.employee.role,
                             'tasks': [],
                             'user': self.user.pk}]}

        self.assertEqual(result, data)


class TaskTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test_user@email.com", username="test_user")
        self.client.force_authenticate(user=self.user)
        self.employee = Employee.objects.create(fullname="Супервайзеров Аркадий Витальевич",
                                                user=self.user,
                                                is_supervisor=True
                                                )
        self.date = timezone.now() + timedelta(hours=1)
        self.first_task = Task.objects.create(title="Купить подарки для продавцов",
                                              deadline=self.date,
                                              executor=self.employee,
                                              status="started"
                                              )
        self.second_task = Task.objects.create(title="Забрать подарки для продавцов",
                                               deadline=self.date,
                                               parental_task=self.first_task
                                               )

    def test_rask_create(self):
        url = reverse("tasks:task-create")
        data = {"title": "Отправить документы в Сибирь", "deadline": self.date}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.all().count(), 3)

    def test_task_retrieve(self):
        url = reverse("tasks:task-detail", args=(self.first_task.pk,))
        response = self.client.get(url)
        result = response.json()
        # data = {'attachment': None,
        #         'comment': None,
        #         'deadline': self.task.deadline.strftime('%Y-%m-%d %H:%M:%S %Z'),
        #         'description': None,
        #         'executor': 1,
        #         'id': 1,
        #         'parental_task': None,
        #         'status': 'created',
        #         'title': 'Забрать подарки для продавцов'}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('title'), self.first_task.title)

    def test_task_list(self):
        response = self.client.get('/tasks/')
        result = response.json()
        self.assertEqual(result.get('count'), 2)

    def test_task_update(self):
        url = reverse("tasks:task-update", args=(self.first_task.pk,))
        data = {"executor": self.employee.pk}
        response = self.client.patch(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("status"), 'started')

    def test_task_delete(self):
        url = reverse("tasks:task-delete", args=(self.second_task.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.all().count(), 1)

    # def test_task_urgent_list(self):
    #     response = self.client.get('/tasks/urgent/')
    #     result = response.json()
    #     print(self.first_task.status)
    #     print(self.second_task.status)
    #     self.assertEqual(result.get('title'), self.second_task.title)
