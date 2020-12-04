from django.db import models

class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    keyword = models.CharField(max_length=500, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    contact_info = models.TextField(null=True, blank=True)
    company_logo = models.ImageField(upload_to='logo', null=True, blank=True)
    company_logo_text = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=60, null=True, blank=True)
    email = models.EmailField(max_length=250, null=True, blank=True)
    facebook = models.URLField(max_length=300, null=True, blank=True)
    youtube = models.URLField(max_length=300, null=True, blank=True)
    twitter = models.URLField(max_length=300, null=True, blank=True)
    instagram = models.URLField(max_length=300, null=True, blank=True)
    linkedin = models.URLField(max_length=300, null=True, blank=True)
    google_plus = models.URLField(max_length=300, null=True, blank=True)
    smtpserver = models.CharField(max_length=50, null=True, blank=True)
    smtpemail = models.EmailField(max_length=250, null=True, blank=True)
    smtppassword = models.CharField(max_length=250, null=True, blank=True)
    smtpport = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=5, choices=STATUS, default='True')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
