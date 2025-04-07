from django.core.cache import cache
from django.db.models import Count, Q
from .models import Employee, Task


def get_least_busy_employee(parental_task_id):
    """Возвращает из БД первого найденного сотрудника с наименьшим количеством задач или сотрудника,
    выполняющего parental_task, если ему назначено максимум на 2 задачи больше, чем у первого.
    Если один из найденных сотрудников с наименьшим количеством задач является исполнителем parental_task,
    он будет выбран приоритетным исполнителем."""

    least_busy_cache_key = 'least_busy_employee'
    parental_tasks_cache_key = f'parental_executor_tasks_count_{parental_task_id}'
    parental_executor_cache_key = f'parental_executor_{parental_task_id}'

    least_busy_employee = cache.get(least_busy_cache_key)

    if least_busy_employee is None:
        employees = Employee.objects.annotate(task_count=Count('tasks', filter=Q(tasks__status='started')))
        least_busy_employee = employees.order_by('task_count').first()
        cache.set(least_busy_cache_key, least_busy_employee, timeout=900)

    parental_executor = cache.get(parental_executor_cache_key)
    if parental_executor == least_busy_employee:  # доработать!
        return parental_executor

    else:
        parental_executor_tasks_count = cache.get(parental_tasks_cache_key)
        if parental_executor_tasks_count is None:
            parental_task = Task.objects.get(id=parental_task_id)
            parental_executor = parental_task.executor
            parental_executor_tasks_count = Task.objects.filter(executor=parental_executor, status='started').count()
            cache.set(parental_executor_cache_key, parental_executor, timeout=900)
            cache.set(parental_tasks_cache_key, parental_executor_tasks_count, timeout=900)

        min_task_count = least_busy_employee.tasks.count()

        if parental_executor_tasks_count <= min_task_count + 2:
            return parental_executor
        return least_busy_employee
