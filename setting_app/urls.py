from django.urls import path
from . import views

app_name = 'setting'

urlpatterns = [
    path('download_pdf_file/', views.download_pdf_file, name='download_pdf_file'),
]
