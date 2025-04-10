from django.db.models import Count, Q

from .models import Employee, Task


def get_least_busy_employee(parental_task_id):
    """Возвращает из БД первого найденного сотрудника с наименьшим количеством задач или сотрудника,
    выполняющего parental_task, если ему назначено максимум на 2 задачи больше, чем у первого.
    Если один из найденных сотрудников с наименьшим количеством задач является исполнителем parental_task,
    он будет выбран приоритетным исполнителем."""

    employees = Employee.objects.filter(is_supervisor=False).annotate(
        task_count=Count('tasks', filter=Q(tasks__status='started'))
    )
    least_busy_employee = employees.order_by('task_count').first()
    parental_task = Task.objects.get(id=parental_task_id)
    parental_executor = parental_task.executor
    if parental_executor == least_busy_employee:
        return parental_executor
    else:
        parental_executor_tasks_count = Task.objects.filter(executor=parental_executor, status='started').count()
        min_task_count = least_busy_employee.tasks.count()
        if parental_executor_tasks_count <= min_task_count + 2:
            return parental_executor
        return least_busy_employee
