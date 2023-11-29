from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,LoginForm,BlogPostForm
from .models import PatientProfile, DoctorProfile,CustomUser,BlogPost

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

#view for blog list
def blog_list(request):
    # Fetch all published blog posts (not marked as draft)
    blog_posts = BlogPost.objects.filter(is_draft=False)
    return render(request, 'myapp/blog_list.html', {'blog_posts': blog_posts})

#view to post blog
def add_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = CustomUser.objects.get(pk=request.user.pk)
            blog_post.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'myapp/add_blog_post.html', {'form': form})

