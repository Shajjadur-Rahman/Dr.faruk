from django.db import models
from django.conf import settings
from django.template.defaultfilters import truncatechars


class Todo(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Completed', 'Completed'),
        ('Trash', 'Trash'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    task = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    task_start = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


    @property
    def sliced_task_description(self):
        return truncatechars(self.task, 100)

