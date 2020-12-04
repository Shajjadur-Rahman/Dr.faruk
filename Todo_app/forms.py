from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        self.fields['task'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Write task detail'})

    class Meta:
        model = Todo
        fields = ['task', ]
