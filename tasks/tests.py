from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Employee, Task
from users.models import User


class EmployeeTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test_user@email.com", username="test_user")
        self.client.force_authenticate(user=self.user)
        self.super_employee = Employee.objects.create(fullname="Супервайзеров Аркадий Витальевич",
                                                      user=self.user,
                                                      is_supervisor=True
                                                      )
        self.employee = Employee.objects.create(fullname="Кандидатов Иосиф Петрович",
                                                user=self.user
                                                )

    def test_employee_create(self):
        """Тестирование создания пользователя"""

        url = reverse("tasks:employee-list")
        data = {"fullname": "Тестов Тест Тестович", "user": 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.all().count(), 3)

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
        self.assertEqual(Employee.objects.all().count(), 1)

    def test_employees_list(self):
        url = reverse("tasks:employee-list")
        response = self.client.get(url)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('count'), 2)

    def test_employees_busy_list(self):
        url = reverse("tasks:employee-busy")
        response = self.client.get(url)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {'id': self.employee.pk, 'fullname': self.employee.fullname, 'department': None, 'role': None,
                     'active_tasks': self.employee.tasks.filter(status='started').count(), 'tasks': []}]}

        self.assertEqual(result, data)


class TaskTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test_user@email.com", username="test_user")
        self.client.force_authenticate(user=self.user)
        self.super_employee = Employee.objects.create(fullname="Супервайзеров Аркадий Витальевич",
                                                      user=self.user,
                                                      is_supervisor=True
                                                      )
        self.employee = Employee.objects.create(fullname="Кандидатов Иосиф Петрович",
                                                user=self.user
                                                )
        self.date = timezone.now() + timedelta(hours=1)
        self.first_task = Task.objects.create(title="test1",
                                              deadline=self.date,
                                              executor=self.employee,
                                              status="started"
                                              )
        self.second_task = Task.objects.create(title="test2",
                                               deadline=self.date,
                                               parental_task=self.first_task
                                               )

    def test_task_create(self):
        url = reverse("tasks:task-create")
        data = {"title": "Отправить документы в Сибирь", "deadline": self.date, "executor": self.employee.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.all().count(), 3)

    def test_task_retrieve(self):
        url = reverse("tasks:task-detail", args=(self.first_task.pk,))
        response = self.client.get(url)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('title'), self.first_task.title)

    def test_task_list(self):
        response = self.client.get('/tasks/')
        result = response.json()
        self.assertEqual(result.get('count'), 2)

    def test_task_update(self):
        test_task = Task.objects.create(title="Тестовая задача",
                                        deadline=self.date,
                                        executor=self.employee,
                                        )
        url = reverse("tasks:task-update", args=(test_task.pk,))

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

    def test_task_urgent_list(self):
        response = self.client.get('/tasks/urgent/')
        result = response.json()
        self.assertEqual(result.get('count'), 1)

    def test_task_urgent_list_less_busy_employee(self):
        self.third_employee = Employee.objects.create(fullname="Новичков Валентин Михайлович",
                                                      user=self.user
                                                      )
        self.third_task = Task.objects.create(title="test3",
                                              deadline=self.date,
                                              executor=self.employee,
                                              status="started"
                                              )
        self.another_task = Task.objects.create(title="test4",
                                                deadline=self.date,
                                                executor=self.employee,
                                                status="started"
                                                )
        response = self.client.get('/tasks/urgent/')
        result = response.json()
        self.assertEqual(result.get('count'), 1)
