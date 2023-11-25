from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,LoginForm
from .models import PatientProfile, DoctorProfile,CustomUser

def home(request):
    return render(request,'myapp/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            if user.is_patient():
                patient_profile = PatientProfile(user=user)
                patient_profile.save()
            elif user.is_doctor():
                doctor_profile = DoctorProfile(user=user)
                doctor_profile.save()

            login(request, user)

            if user.is_patient():
                return redirect('patient_dashboard')
            elif user.is_doctor():
                return redirect('doctor_dashboard')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                if user.is_patient():
                    return redirect('patient_dashboard')
                elif user.is_doctor():
                    return redirect('doctor_dashboard')
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {'form': form})
@login_required
def patient_dash(request):
    user = CustomUser.objects.get(pk=request.user.pk)
    return render(request,'myapp/patient_dashboard.html',{'user':user})
@login_required
def doctor_dash(request):
    user = CustomUser.objects.get(pk=request.user.pk)
    return render(request,'myapp/doctor_dashboard.html',{'user':user})