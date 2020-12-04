from .models import User

def all_user():
    users = User.objects.all()
    pass
