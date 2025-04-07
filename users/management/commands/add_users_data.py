from django.core.management.base import BaseCommand
from django.core.management import call_command

from tasks.models import Task, Employee
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Task.objects.all().delete()
        Employee.objects.all().delete()
        User.objects.all().delete()

        call_command('loaddata', 'users_fixture.json')
        self.stdout.write('Данные из фикстуры Users успешно загружены')

        call_command('loaddata', 'tasks_fixture.json')
        self.stdout.write('Данные из фикстуры Tasks успешно загружены')
