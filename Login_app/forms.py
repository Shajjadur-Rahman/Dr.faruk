from django.forms import TextInput, PasswordInput

from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import Group
from django import forms


class SignUpForm(UserCreationForm):
    role = forms.ModelChoiceField(queryset=Group.objects.all())

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Input your email', 'id': 'exampleInputEmail1',
                                                  'class': 'form-control'}),
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password', 'id': 'exampleInputPassword1',
                                                      'class': 'form-control'}),
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password', 'id': 'exampleInputPassword2',
                                                      'class': 'form-control'}),

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)



    def save(self, commit=True):
        role = self.cleaned_data.pop('role')
        u = super().save()
        u.groups.set([role])
        u.save()
        return u



class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'input your email', 'id': 'exampleInputEmail1',
                                                       'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password', 'id': 'exampleInputPassword1',
                                                           'class': 'form-control'}))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.error_messages = {'required': '{fieldname} is required'.format(
                fieldname=field.label)}


class LoggedInUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'password']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'mobile_no', 'fb_id', 'image', ]

