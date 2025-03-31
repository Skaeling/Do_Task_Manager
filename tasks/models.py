from django.db import models
from config.settings import AUTH_USER_MODEL


class Employee(models.Model):
    fullname = models.CharField(max_length=50, verbose_name='ФИО')
    position = models.CharField(max_length=50, null=True, blank=True, verbose_name='Должность')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employees',
                             verbose_name="Пользователь")
    is_supervisor = models.BooleanField(default=False, verbose_name='Супервизор')

    def __str__(self):
        return f'{self.fullname} - {self.position}'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Task(models.Model):
    CREATED = 'created'
    STARTED = 'started'
    UNDER_REVIEW = 'under_review'
    RESUBMIT = 'resubmit'
    COMPLETED = 'completed'
    DELAYED = 'delayed'
    CANCELLED = 'cancelled'

    TASK_STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (STARTED, 'В работе'),
        (UNDER_REVIEW, 'На проверке'),
        (RESUBMIT, 'Требует доработки'),
        (COMPLETED, 'Завершена'),
        (DELAYED, 'Отложена'),
        (CANCELLED, 'Отменена'),
    ]

    title = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name='Описание')
    parental_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks',
                                      verbose_name='Родительская задача')
    executor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks',
                                 verbose_name="Исполнитель")
    deadline = models.DateTimeField(verbose_name='Срок исполнения')
    status = models.CharField(max_length=13, choices=TASK_STATUS_CHOICES, default=CREATED, verbose_name='Статус')
    attachment = models.FileField(upload_to='task_files/%Y/%m/%d/', blank=True, null=True)
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f'Задача: {self.title} к {self.deadline}. Статус: {self.status}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
