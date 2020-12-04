import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

from .models import Todo
from .forms import TodoForm
from Dashboard_app.decorators import allowed_users
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def create_task(request):
    form = TodoForm()
    if request.method == 'POST':
        task_start = str(request.POST.get('task_start'))
        format_task_start = datetime.strptime(task_start, '%m/%d/%Y %I:%M %p')
        form = TodoForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user
            form_obj.task_start = format_task_start
            form_obj.save()
            messages.info(request, 'Task created successfully !')
            return HttpResponseRedirect(reverse('task:all-tasks-schedule'))

    context = {'form': form}
    return render(request, 'todo_app/create_task.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def all_tasks_schedule(request):
    all_tasks = Todo.objects.filter(user=request.user, status='New').order_by('task_start')
    context = {'all_tasks': all_tasks}
    return render(request, 'todo_app/all_tasks_schedule.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def task_detail(request, task_id):
    try:
        task = Todo.objects.get(pk=task_id, user=request.user, status='New')
    except Exception as e:
        messages.warning(request, 'Task query not exist !')
        return HttpResponseRedirect(reverse('task:all-tasks-schedule'))
    context = {'task': task}
    return render(request, 'todo_app/task_detail.html', context)





@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def task_complete(request):
    body = json.loads(request.body)
    task = Todo.objects.get(pk=body['task_id'])
    task.status = 'Completed'
    task.save()
    return Response('ok', 'completed')


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def show_completed_tasks(request):
    tasks = Todo.objects.filter(user=request.user, status='Completed')
    context = {'tasks': tasks}
    return render(request, 'todo_app/show_completed_tasks.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def show_completed_tasks_detail(request, task_id):
    try:
        task = Todo.objects.get(pk=task_id, user=request.user, status='Completed')
    except Exception as e:
        messages.warning(request, 'Task query not exist !')
        return HttpResponseRedirect(reverse('task:all-tasks-schedule'))
    context = {'task': task}
    return render(request, 'todo_app/show_completed_tasks_detail.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager'])
def delete_task(request, task_id):
    try:
        task = Todo.objects.get(pk=task_id, user=request.user)
    except Exception as e:
        messages.warning(request, 'Task query not exist !')
        return HttpResponseRedirect(reverse('task:all-tasks-schedule'))
    task.delete()
    messages.warning(request, 'Task deleted from database !')
    return HttpResponseRedirect(reverse('task:show-completed-tasks'))









