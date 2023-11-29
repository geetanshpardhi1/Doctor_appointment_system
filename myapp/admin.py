from django.contrib import admin
from .models import PatientProfile,DoctorProfile,CustomUser,BlogPost
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(BlogPost)