from django.db.models import Count
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout
from hospital.forms import ProfileForm, AdditionalProfileForm, AppointmentForm, ChangePasswordForm
from hospital.models import Profile, Appointment, Medical_Record
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from datetime import date, timedelta
import datetime
from hospital.utility import render_to_pdf
from django.contrib.auth.models import User


def patient_dashboard(request):

    if request.user.is_authenticated:
        appointment_data = Appointment.objects.filter(user=request.user).order_by('-app_date')
        prescription_data = Medical_Record.objects.values('user','doctor_name', 'date').filter(user=request.user).annotate(Count('id')).order_by()
        print(prescription_data)
        return render(request, 'hospital/patient/dashboard.html', {'appointment_data': appointment_data, 'prescription_data': prescription_data})
    
    else:
        return redirect('/')

def patient_profile(request):
    if request.user.is_authenticated:
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
                return redirect('/patient/profile/')
            else:
                return render(request, 'hospital/patient/profile.html',{'profile_form': profile_form, 'add_profile_form': add_profile_form })
        
        else:
            return render(request, 'hospital/patient/profile.html',{'profile_form': profile_form, 'add_profile_form': add_profile_form })
    else:
        return redirect('/')

def patient_appointment(request):

    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            appointment_form = AppointmentForm(request.POST)

            if appointment_form.is_valid():
                doctor = request.POST['doctor']
                doctor_name = doctor.split('|')[0]
                department_name = doctor.split('|')[1]
                user = request.user
                full_name = request.user.first_name +' '+request.user.last_name
                mobile = user.profile.mobile
                note_date = appointment_form.cleaned_data.get('app_date')
                app_count = Appointment.objects.filter(doctor_name=doctor_name, app_date=appointment_form.cleaned_data.get('app_date')).count()

                if user.profile.mobile == '' and user.profile.address == 'NULL':
                    messages.warning(request, 'Complete profile information for appointment.')
                
                else:
                    if app_count < 10:
                        app_no = app_count + 1
                        
                        check_data = Appointment.objects.filter(user=user, app_date=note_date).count()
                        if check_data == 0:
                            data = Appointment(user=user, full_name=full_name, mobile=mobile, app_date=note_date, doctor_name=doctor_name, department=department_name, appointment_no=app_no)
                            data.save()
                            messages.success(request, f'Appointment is successfully created on date {note_date} and <strong>Appointment no. is {app_no}</strong>.')
                        
                        else:
                            messages.success(request, f'Appointment is already booked on date {note_date}')
                    
                    else:
                        messages.success(request, f'Appointment is not available on date {note_date}, please select another date for appointment.')

                return redirect('/patient/appointment/')
            
            else:
                doctor_list = Profile.objects.filter(user_type= 'Doctor').all()
                return render(request, 'hospital/patient/appointment.html', {'appointment_form': appointment_form, 'doctor_list': doctor_list})

        else:
            appointment_form = AppointmentForm()
            doctor_list = Profile.objects.filter(user_type= 'Doctor').all() 
            return render(request, 'hospital/patient/appointment.html', {'appointment_form': appointment_form, 'doctor_list': doctor_list})
    else:
        return redirect('/')

def patient_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(user = request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password is successfully changed.')
                return redirect('/patient/passwordchange/')
            
            else:
                return render(request, 'hospital/patient/passwordchange.html', {'form': form})        
        
        else:
            form = ChangePasswordForm(user = request.user)
            return render(request, 'hospital/patient/passwordchange.html', {'form': form})
    
    else:
        return redirect('/')

def view_prescription(request, user_info, doctor_name, date):
    if request.user.is_authenticated:
        rec_date = datetime.datetime.strptime(date, "%m-%d-%Y").date()
        user_detail = User.objects.values('first_name', 'last_name').filter(username=user_info)
        records = Medical_Record.objects.filter(user = user_info, doctor_name=doctor_name, date=rec_date)

        data = {
            'date' : date,
            'records': records,
            'user_data' : user_detail,
            'doc_name' : doctor_name,
        }
        
        pdf = render_to_pdf('hospital/doctor/showrecords.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return redirect('/')

def patient_logout(request):
    logout(request)
    return redirect('/')