from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime, timedelta
from .forms import SignUpForm,LoginForm,BlogPostForm,AppointmentForm
from .models import PatientProfile, DoctorProfile,CustomUser,BlogPost,Appointment
from .google_calendars import create_calendar_event


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
    blog_posts = BlogPost.objects.filter(is_draft=False)
    #for contexting them categorically
    blog_posts_by_category = BlogPost.objects.filter(is_draft=False).values('category').annotate(count=Count('id'))
    return render(request,'myapp/patient_dashboard.html',{'user':user,'blog_posts': blog_posts,'blog_posts_by_category': blog_posts_by_category})
@login_required
def doctor_dash(request):
    user = CustomUser.objects.get(pk=request.user.pk)
    return render(request,'myapp/doctor_dashboard.html',{'user':user})

#view for blog list
def blog_list(request):
    blog_posts = BlogPost.objects.filter(is_draft=False)
    #for contexting them categorically
    blog_posts_by_category = BlogPost.objects.filter(is_draft=False).values('category').annotate(count=Count('id'))
    return render(request, 'myapp/blog_list.html', {'blog_posts_by_category': blog_posts_by_category,'blog_posts': blog_posts})


#view to post blog
def add_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = CustomUser.objects.get(pk=request.user.pk)
            blog_post.save()
            return redirect('posted_blogs')
    else:
        form = BlogPostForm()
    return render(request, 'myapp/add_blog_post.html', {'form': form})

#for detail view of each blog
def blog_detail(request, blog_id):
    blog_post = get_object_or_404(BlogPost, id=blog_id)
    return render(request, 'myapp/blog_detail.html', {'blog_post': blog_post})

#draft blogs
def doctor_draft_blogs(request):

    draft_blogs = BlogPost.objects.filter(author=request.user, is_draft=True)

    return render(request, 'myapp/draft_blogs.html', {'draft_blogs': draft_blogs})

#view personal posted blogs
def personal_blog_list(request):
    blog_posts = BlogPost.objects.filter(author=request.user,is_draft=False)
    return render(request, 'myapp/posted_blogs.html', {'blog_posts': blog_posts})

#view for listing all doctors
@login_required
def doctor_list(request):
    doctors = CustomUser.objects.filter(user_role='doctor')
    return render(request, 'myapp/doctor_list.html', {'doctors': doctors})

#view for book appointment
@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(CustomUser, id=doctor_id, user_role='doctor')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.save()

            # Call the function to create a calendar event
            create_calendar_event(
                doctor_email=doctor.email,
                patient_name=request.user.get_full_name(),
                appointment_date=str(appointment.appointment_date),
                start_time=str(appointment.start_time),
                end_time=str(appointment.end_time)
            )

            return redirect('appointment_confirmation', appointment_id=appointment.id)
    else:
        form = AppointmentForm()

    return render(request, 'myapp/book_appointment.html', {'form': form, 'doctor': doctor})

#view for seeing appointments for patient user only
@login_required
def appointment_confirmation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    return render(request, 'myapp/appointment_confirmation.html', {'appointment': appointment})


@login_required
def patient_appointments(request):
    user = request.user
    appointments = Appointment.objects.filter(patient=user)
    return render(request, 'myapp/patient_appointments.html', {'appointments': appointments})