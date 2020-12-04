from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    path('create-task/', views.create_task, name='create-task'),
    path('all-tasks-schedule/', views.all_tasks_schedule, name='all-tasks-schedule'),
    path('task-detail/<int:task_id>', views.task_detail, name='task-detail'),
    path('task-complete/', views.task_complete, name='task-complete'),
    path('show-completed-tasks/', views.show_completed_tasks, name='show-completed-tasks'),
    path('completed-task-detail/<int:task_id>', views.show_completed_tasks_detail, name='completed-task-detail'),
    path('delete-task/<int:task_id>', views.delete_task, name='delete-task'),
]
