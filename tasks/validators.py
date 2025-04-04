from datetime import timedelta
from .models import Task
from rest_framework.serializers import ValidationError
from django.utils import timezone


def validate_deadline(value):
    if timezone.now() >= value:
        raise ValidationError('Срок исполнения задачи не может быть в прошлом!')
    elif value >= timezone.now() + timedelta(days=7):
        raise ValidationError('Срок исполнения задачи не должен превышать 7 дней!')


def validate_executor_tasks(value):
    task_limit = 5
    executor_active_tasks = Task.objects.filter(executor=value, status='started').count()
    if executor_active_tasks >= task_limit:
        raise ValidationError('Превышено количество активных задач у сотрудника, выберете другого')


def validate_attachment_size(value):
    if value.size > 5 * 1024 * 1024:
        raise ValidationError("Файл превышает допустимый размер ( > 5mb )")


class WordsValidator:
    forbidden_phrases = ['срочно', 'asap', '!!!']

    def __init__(self, title_key, description_key, comment_key):
        self.title_key = title_key
        self.description_key = description_key
        self.comment_key = comment_key

    def __call__(self, value):
        title = value.get(self.title_key)
        description = value.get(self.description_key)
        comment = value.get(self.comment_key)

        self._validate_field(title, 'названии')
        self._validate_field(description, 'описании')
        self._validate_field(comment, 'комментарии')

    def _validate_field(self, field_value, field_name):
        if field_value and any(phrase in field_value.lower() for phrase in self.forbidden_phrases):
            raise ValidationError(f'Использованы нерекомендуемые выражения в {field_name}')
