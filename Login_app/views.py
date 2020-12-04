from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .forms import SignUpForm, LoginForm, ProfileForm, LoggedInUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .decorators import unauthenticated_user
from django.contrib import messages
from Login_app.models import User
from django.contrib.auth.models import Group
from Dashboard_app.decorators import allowed_users
from .models import Profile
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver





def sign_up_user(request):
    form = SignUpForm()
    user_obj = User()
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        try:
            user = User.objects.get(email=email)
            messages.warning(request, f'Sorry "{user}"  have already an account !')
            context = {'form': form}
            return render(request, 'account/signup.html', context)
        except Exception as e:
            if password1 == password2:
                user_obj.email = email
                user_obj.set_password(password1)
                user_obj.set_password(password2)
                user_obj.save()
                group = Group.objects.get(name='Remove-access')
                user_obj.groups.add(group)

                return HttpResponseRedirect(reverse('Login_app:login'))
            else:
                messages.warning(request, 'Password mismatch ! Tray again..............')
    context = {'form': form}
    return render(request, 'account/signup.html', context)


def login_user(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        username = request.POST.get('username')
        try:
            is_active = User.objects.get(email=username).is_active
            if is_active:
                if form.is_valid():
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password')
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return HttpResponseRedirect(reverse('Dashboard:home'))
                else:
                    messages.warning(request, 'Invalid email or password !')
            else:
                messages.warning(request,
                                 f'Sorry {username},\
                                  You are not authorized to login this site for complicated issue !\
                                   Contact with Admin through flowing email .............\
                                    "shaturngbd@gmail.com"')
        except:
            messages.warning(request, 'Invalid email or password !')

    context = {
        'form': form
    }
    return render(request, 'account/login.html', context)


@login_required
def log_out_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_app:login'))


@login_required
@allowed_users(allowed_roles=['Admin', 'Accountant', 'Manager', 'Remove-access'])
def user_profile(request, user_id):
    try:
        profile = User.objects.get(pk=user_id)
    except Exception as e:
        messages.warning(request, 'Employee does not exists !')
        return HttpResponseRedirect(reverse('Dashboard:home'))
    context = {'profile': profile}
    return render(request, 'dashboard_app/profile.html', context)


@login_required
def edit_user_profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        profile = Profile.objects.get(user_id=user.pk)
    except Exception as e:
        messages.warning(request, 'Employee does not exists !')
        return HttpResponseRedirect(reverse('Dashboard:home'))
    form = LoggedInUserChangeForm(instance=user)
    p_form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = LoggedInUserChangeForm(request.POST, instance=user)
        p_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully !')
            return HttpResponseRedirect(reverse('Login_app:profile', kwargs={'user_id': user_id}))
    context = {'profile': profile, 'form': form, 'p_form': p_form}
    return render(request, 'dashboard_app/edit_profile.html', context)


@login_required
def password_change(request):
    current_user = request.user
    form = PasswordChangeForm(current_user)
    if request.method == "POST":
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('app_login:profile'))
    return render(request, 'dashboard_app/password_change.html', context={'form': form, 'current_user': current_user})


@login_required
def change_pro_pic(request):
    return render(request, 'account/change_pro_pic.html')



@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.profile.is_online = True
    user.profile.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.profile.is_online = False
    user.profile.save()
