from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout
from hospital.forms import ProfileForm, AdditionalProfileForm, AppointmentForm, ChangePasswordForm, DoctorProfileForm
from hospital.models import Profile, Appointment, Medical_Record
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from datetime import date, timedelta
import datetime
from django.contrib.auth.models import User
from hospital.utility import render_to_pdf


def doctor_dashboard(request):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Doctor':
            doctor_name = request.user.first_name +' '+request.user.last_name
            appointment_data = Appointment.objects.filter(doctor_name=doctor_name, app_date=date.today())
            return render(request, 'hospital/doctor/dashboard.html', {'appointment_data': appointment_data})
        else:
            return redirect('/')

    else:
        return redirect('/')

def doctor_appointments(request):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Doctor':
            if request.method == 'POST':
                get_date = request.POST.get('date')
                doctor_name = request.user.first_name +' '+request.user.last_name
                app_list = Appointment.objects.filter(doctor_name=doctor_name, app_date=get_date).all()
                return render(request, 'hospital/doctor/appointment_list.html', {'app_list': app_list, 'show_date': get_date})
            else:
                show_date = date.today().strftime("%Y-%m-%d")

                doctor_name = request.user.first_name +' '+request.user.last_name
                app_list = Appointment.objects.filter(doctor_name=doctor_name, app_date=date.today()).all()
                return render(request, 'hospital/doctor/appointment_list.html', {'app_list': app_list, 'show_date': show_date})

        else:
            return redirect('/')    

    else:
        return redirect('/')

def doctor_patients(request):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Doctor':
            doctor_name = request.user.first_name +' '+request.user.last_name
            patient_list = Appointment.objects.filter(doctor_name=doctor_name).values('full_name','mobile', 'user').annotate(Count('id')).order_by().filter(id__count__gt=1)
            return render(request, 'hospital/doctor/patient_list.html', {'patient_list': patient_list})
        else:
            return redirect('/')
    else:
        return redirect('/')

def doctor_profile(request):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Doctor':
            user = request.user
            data = {
            'first_name': request.user.first_name,
            'last_name' : request.user.last_name,
            'email' : request.user.email,
            'age' : user.profile.age,
            'blood_group' : user.profile.blood_group,
            'address' : user.profile.address,
            'mobile' : user.profile.mobile,
            'department' : user.profile.department
            }

            profile_form = ProfileForm(initial= data)
            add_profile_form = DoctorProfileForm(initial= data)

            if request.method == 'POST':
                profile_form = ProfileForm(data = request.POST, instance = request.user)
                add_profile_form = DoctorProfileForm(request.POST, request.FILES, instance = request.user)
                if add_profile_form.is_valid():
                    user = profile_form.save(commit=False)
                    user.save()
                    add_profile = Profile.objects.get(pk=user.profile.id)
                    add_profile.department = add_profile_form.cleaned_data['department']
                    add_profile.address = add_profile_form.cleaned_data['address']
                    add_profile.mobile = add_profile_form.cleaned_data['mobile']
                    add_profile.blood_group = add_profile_form.cleaned_data['blood_group']
                    add_profile.age = add_profile_form.cleaned_data['age']
                    add_profile.profile_pic = add_profile_form.cleaned_data['profile_pic']
                    add_profile.save()
                    messages.success(request, 'Account information successfully updated.')
                    return redirect('/doctor/profile/')
                else:
                    return render(request, 'hospital/doctor/profile.html',{'profile_form': profile_form, 'add_profile_form': add_profile_form })
            
            else:
                return render(request, 'hospital/doctor/profile.html',{'profile_form': profile_form, 'add_profile_form': add_profile_form })
        else:
            return redirect('/')
    else:
        return redirect('/')

def doctor_password(request):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Doctor':
            if request.method == 'POST':
                form = ChangePasswordForm(user = request.user, data = request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                    messages.success(request, 'Password is successfully changed.')
                    return redirect('/doctor/passwordchange/')
                
                else:
                    return render(request, 'hospital/doctor/passwordchange.html', {'form': form})        
            
            else:
                form = ChangePasswordForm(user = request.user)
                return render(request, 'hospital/doctor/passwordchange.html', {'form': form})
        else:
            return redirect('/')
    else:
        return redirect('/')

def appointment_confirm(request, id):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Doctor':
            data = Appointment.objects.get(pk=id)
            data.appointment_status = True
            messages.success(request, f'Appointment successfull confirm for <strong>"{data.full_name}"</strong>.')
            data.save()
            return redirect('/doctor/appointment_list/')
        else:
            return redirect('/')
    else:
        return redirect('/')

def doctor_prescription(request, id):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Doctor':
            if request.method == 'POST':
                user = request.POST['user']
                doctorname = request.POST['doc_name']
                dept = request.POST['dept']
                count = int(request.POST['input_counter'])
                for i in range(1, count+1):
                    med_name = request.POST['prescription_'+str(i)]
                    day = request.POST['days_'+str(i)]
                    today = date.today()
                    data = Medical_Record(user=user, doctor_name=doctorname, department=dept, date=today, prescription=med_name, days=day)
                    data.save()
                messages.success(request, 'Prescription successfully save.')
                return HttpResponseRedirect(request.path_info)
            
            else:
                data = Appointment.objects.filter(pk=id)
                return render(request, 'hospital/doctor/prescription.html', {'data': data})
        else:
            return redirect('/')
    else:
        return redirect('/')

def view_record(request, user_info):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Doctor':
            user = request.user
            doctorname = user.first_name +" "+ user.last_name
            patient_data = User.objects.filter(username=user_info)
            # records = Medical_Record.objects.values('user', 'date').filter(user=user_info, doctor_name=doctorname)
            records = Medical_Record.objects.values('user', 'date').filter(user=user_info, doctor_name=doctorname).annotate(Count('id')).order_by()
            # records = Medical_Record.objects.raw('SELECT COUNT (*), date from hospital_medical_record GROUP BY date')
            return render(request, 'hospital/doctor/viewrecord.html', {'patient_data': patient_data, 'records': records})
        else:
            return redirect('/')
    else:
        return redirect('/')

def view_prescription(request, user_info, date):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Doctor':
            rec_date = datetime.datetime.strptime(date, "%m-%d-%Y").date()
            user_detail = User.objects.values('first_name', 'last_name').filter(username=user_info)
            doc_name = request.user.first_name +" "+request.user.last_name
            records = Medical_Record.objects.filter(user = user_info, doctor_name=doc_name, date=rec_date)

            data = {
                'date' : date,
                'records': records,
                'user_data' : user_detail,
                'doc_name' : doc_name,
                'name' : 'Nishikant Sonkusare'
            }
            
            pdf = render_to_pdf('hospital/doctor/showrecords.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            return redirect('/')
    else:
        return redirect('/')

def doctor_logout(request):
    logout(request)
    return redirect('/')