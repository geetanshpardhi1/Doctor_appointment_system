from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('patient-dashboard/',views.patient_dash, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dash, name='doctor_dashboard'),
    path('blog/',views.blog_list, name='blog_list'),
    path('blog/add/',views.add_blog_post, name='add_blog_post'),
]
