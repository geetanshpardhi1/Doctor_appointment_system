from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]
    
    user_role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    def is_patient(self):
        return self.user_role == 'patient'

    def is_doctor(self):
        return self.user_role == 'doctor'

class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   
class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  
#model for blogs
class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('Mental Health', 'Mental Health'),
        ('Heart Disease', 'Heart Disease'),
        ('Covid19', 'Covid19'),
        ('Immunization', 'Immunization'),
       #we can add more categories.
    ]

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    summary = models.TextField()
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=False)

    def truncated_summary(self):
        return ' '.join(self.summary.split()[:15]) + '...' if len(self.summary.split()) > 15 else self.summary

    def __str__(self):
        return self.title