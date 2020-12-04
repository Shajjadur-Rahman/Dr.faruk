from .models import Todo



def all_tasks(request):
    tasks = Todo.objects.filter(status='New').order_by('-task_start')[:5]
    return {'tasks': tasks}
