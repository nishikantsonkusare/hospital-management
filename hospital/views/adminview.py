from django.db.models import Count
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout
from hospital.forms import ProfileForm, AdditionalProfileForm, AppointmentForm, ChangePasswordForm, DoctorProfileForm
from hospital.models import Profile, Appointment, Medical_Record
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.db.models import Q
from itertools import chain

def admin_dashboard(request):
    if request.user.is_authenticated:
        if request.session["user_type"] == True:
            emp_count = Profile.objects.filter(user_type__in= ('Doctor','Receptionist')).count()
            patient_count = Profile.objects.filter(user_type= 'Patient').count()
            pending_user = Profile.objects.filter(user_type__in= ('Doctor','Receptionist')).filter(is_approved=False).count()
            doctor_list = Profile.objects.filter(user_type='Doctor')

            context = {
                'emp_count' : emp_count,
                'patient_count' : patient_count,
                'pending_user' : pending_user,
                'doctor_list' : doctor_list,
            }
            return render(request, 'hospital/admin/dashboard.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def admin_employee(request):
    if request.user.is_authenticated:
        if request.session["user_type"] == True:
            if request.method == 'POST':
                txt = request.POST['get_text']
                search_by = request.POST['search_by']
                if txt:
                    if search_by == 'Name':
                        new_data = User.objects.filter(Q(first_name__icontains=txt) | Q(last_name__icontains=txt))
                        emp = []
                        for d in new_data:
                            emp.append(d.profile)

                    if search_by == 'Mobile':
                        emp = Profile.objects.filter(mobile__icontains=txt).filter(user_type__in= ('Doctor','Receptionist'))
                    
                    if search_by == 'All':
                        emp = Profile.objects.filter(user_type__in= ('Doctor','Receptionist'))

                    return render(request, 'hospital/admin/employee_list.html', {'emp': emp})


                else:
                    emp = Profile.objects.filter(user_type__in= ('Doctor','Receptionist'))
                    return render(request, 'hospital/admin/employee_list.html', {'emp': emp})    
            else:
                emp = Profile.objects.filter(user_type__in= ('Doctor','Receptionist'))
                return render(request, 'hospital/admin/employee_list.html', {'emp': emp})
        else:
            return redirect('/')
    else:
        return redirect('/')

def admin_appointments(request):
    if request.user.is_authenticated:
        if request.session["user_type"] == True:
            if request.method == 'POST':
                get_date = request.POST.get('date')
                doctor_name = request.POST.get('doctor_name')

                if doctor_name == 'All':
                    show_date = date.today().strftime("%Y-%m-%d")
                    doctor = Profile.objects.filter(user_type='Doctor')
                    app_list = Appointment.objects.filter(app_date=get_date).all()    

                else:
                    doctor = Profile.objects.filter(user_type='Doctor')
                    app_list = Appointment.objects.filter(doctor_name=doctor_name, app_date=get_date).all()
                return render(request, 'hospital/admin/appointment_list.html', {'app_list': app_list, 'show_date': get_date, 'doctor': doctor})

            else:
                show_date = date.today().strftime("%Y-%m-%d")
                doctor = Profile.objects.filter(user_type='Doctor')
                app_list = Appointment.objects.filter(app_date=date.today()).all()
                return render(request, 'hospital/admin/appointment_list.html', {'app_list': app_list, 'show_date': show_date, 'doctor': doctor})
        else:
            return redirect('/')
    else:
        return redirect('/')

def appointment_confirm(request, id):
    if request.user.is_authenticated:
        if request.session["user_type"] == True:
            data = Appointment.objects.get(pk=id)
            data.appointment_status = True
            messages.success(request, f'Appointment successfull confirm for <strong>"{data.full_name}"</strong>.')
            data.save()
            return redirect('/admin/appointment_list/')
        else:
            return redirect('/')
    else:
        return redirect('/')

def admin_patients(request):
    if request.user.is_authenticated:
        if request.session["user_type"] == True:
            if request.method == 'POST':
                txt = request.POST['get_text']
                search_by = request.POST['search_by']
                if txt:
                    if search_by == 'Name':
                        new_data = User.objects.filter(Q(first_name__icontains=txt) | Q(last_name__icontains=txt))
                        emp = []
                        for d in new_data:
                            emp.append(d.profile)

                    if search_by == 'Mobile':
                        emp = Profile.objects.filter(mobile__icontains=txt).filter(user_type='Patient')
                    
                    if search_by == 'All':
                        emp = Profile.objects.filter(user_type='Patient')

                    return render(request, 'hospital/admin/patient_list.html', {'emp': emp})


                else:
                    emp = Profile.objects.filter(user_type='Patient')
                    return render(request, 'hospital/admin/patient_list.html', {'emp': emp})    
            else:
                emp = Profile.objects.filter(user_type='Patient')
                return render(request, 'hospital/admin/patient_list.html', {'emp': emp})
        else:
            return redirect('/')
    else:
        return redirect('/')

def admin_pending_users(request):
    if request.user.is_authenticated:
        if request.session["user_type"] == True:
            user_data = Profile.objects.filter(is_approved=False).filter(user_type__in= ('Doctor','Receptionist'))
            return render(request, 'hospital/admin/pending_user.html', {'user_data': user_data})
        else:
            return redirect('/')
    else:
        return redirect('/')

def admin_user_approved(request, id):
    if request.user.is_authenticated:
        if request.session["user_type"] == True:
            data = Profile.objects.get(pk=id)
            data.is_approved = True
            data.save()
            messages.success(request, f'Appointment successfull confirm for <strong>"{data.user.first_name} {data.user.last_name}"</strong>.')
            return redirect('/admin/pending_users/')
        else:
            return redirect('/')
    else:
        return redirect('/')
def admin_profile(request):
    if request.user.is_authenticated:
        if request.session["user_type"] == True:
            user = request.user
            data = {
            'first_name': request.user.first_name,
            'last_name' : request.user.last_name,
            'email' : request.user.email,
            'age' : user.profile.age,
            'blood_group' : user.profile.blood_group,
            'address' : user.profile.address,
            'mobile' : user.profile.mobile
            }

            profile_form = ProfileForm(initial= data)
            add_profile_form = AdditionalProfileForm(initial= data)

            if request.method == 'POST':
                profile_form = ProfileForm(data = request.POST, instance = request.user)
                add_profile_form = AdditionalProfileForm(request.POST, request.FILES, instance = request.user)
                if add_profile_form.is_valid():
                    user = profile_form.save(commit=False)
                    user.save()
                    add_profile = Profile.objects.get(pk=user.profile.id)
                    add_profile.address = add_profile_form.cleaned_data['address']
                    add_profile.mobile = add_profile_form.cleaned_data['mobile']
                    add_profile.blood_group = add_profile_form.cleaned_data['blood_group']
                    add_profile.age = add_profile_form.cleaned_data['age']
                    add_profile.profile_pic = add_profile_form.cleaned_data['profile_pic']
                    add_profile.save()
                    messages.success(request, 'Account information successfully updated.')
                    return redirect('/admin/profile/')
                else:
                    return render(request, 'hospital/admin/profile.html', {'profile_form': profile_form, 'add_profile_form': add_profile_form })
            
            else:
                return render(request, 'hospital/admin/profile.html',{'profile_form': profile_form, 'add_profile_form': add_profile_form })
        else:
            return redirect('/')
    else:
        return redirect('/')

def admin_password(request):
    if request.user.is_authenticated:
        if request.session["user_type"] == True:
            if request.method == 'POST':
                form = ChangePasswordForm(user = request.user, data = request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                    messages.success(request, 'Password is successfully changed.')
                    return redirect('/admin/passwordchange/')
                
                else:
                    return render(request, 'hospital/admin/passwordchange.html', {'form': form})        
            
            else:
                form = ChangePasswordForm(user = request.user)
                return render(request, 'hospital/admin/passwordchange.html', {'form': form})
        else:
            return redirect('/')
    else:
        return redirect('/')

def doctor_logout(request):
    logout(request)
    return redirect('/')