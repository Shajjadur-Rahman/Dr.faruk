from django.urls import path
from . import views
app_name = 'Login_app'

urlpatterns = [
    path('signup/', views.sign_up_user, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.log_out_user, name='logout'),
    path('profile/<int:user_id>', views.user_profile, name='profile'),
    path('edit-profile/<int:user_id>', views.edit_user_profile, name='edit-profile'),
    path('password/', views.password_change, name='password'),
]
