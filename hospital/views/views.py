from django.shortcuts import render, HttpResponse, redirect
from hospital.forms import NewUserForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from hospital.models import Profile
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Create your views here.

def home(request):

    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser == True:
            return redirect('admin/dashboard/')
        if user.profile.user_type == 'Patient':
            return redirect('patient/dashboard/')
        if user.profile.user_type == 'Doctor':
            return redirect('/doctor/dashboard/')
        if user.profile.user_type == 'Receptionist':
            return redirect('/receptionist/dashboard/')
    

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            # User Authentication
            user = authenticate(username = username, password = password)

            if user.is_superuser == True:
                login(request, user)
                request.session["user_type"] = user.is_superuser
                messages.success(request, 'Login is successfully.')
                return redirect('admin/dashboard')

            # If user is patient then dashboard will views by this function.
            if user.profile.user_type == 'Patient':
                login(request, user)
                messages.success(request, 'Login is successfully.')
                return redirect('patient/dashboard/')

            if user.profile.user_type == 'Doctor':
                if user.profile.is_approved == True:
                    login(request, user)
                    request.session["user_type"] = user.profile.user_type
                    messages.success(request, 'Login is successfully.')
                    return redirect('/doctor/dashboard/')
                else:
                    messages.warning(request, 'Contact administration for approved your login.')
                    return redirect('/')

            if user.profile.user_type == 'Receptionist':
                if user.profile.is_approved == True:
                    login(request, user)
                    request.session["user_type"] = user.profile.user_type
                    messages.success(request, 'Login is successfully.')
                    return redirect('/receptionist/dashboard/')
                else:
                    messages.warning(request, 'Contact administration for approved your login.')
                    return redirect('/')

        else:
            return render(request, 'hospital/home/index.html', {'login_form': login_form})
    else:
        login_form = LoginForm()
        return render(request, 'hospital/home/index.html', {'login_form': login_form})


def register(request):
    if request.method == 'POST':
        register = NewUserForm(request.POST)

        if register.is_valid():
            user = register.save(commit=False)
            user.password = make_password(user.password)
            user_t = request.POST['user_type']
            profile = Profile(user=user, user_type=user_t)
            user.save()
            profile.save()
            messages.success(request, f'"{user.first_name} {user.last_name}" is successfully created.')
            return redirect('/registration/')
        
        else:
            return render(request, 'hospital/home/registration.html', {'register': register})

    else:
        register = NewUserForm()
        return render(request, 'hospital/home/registration.html', {'register': register})

def about(request):
    return render(request, 'hospital/home/about.html')

def contact(request):
    return render(request, 'hospital/home/contact.html')