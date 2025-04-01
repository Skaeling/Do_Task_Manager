from django.core.management.base import BaseCommand
from django.core.management import call_command
from tasks.models import Employee, Task


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Employee.objects.all().delete()
        Task.objects.all().delete()

        call_command('loaddata', 'tasks_fixture.json')
        self.stdout.write('Данные из фикстуры успешно загружены')
