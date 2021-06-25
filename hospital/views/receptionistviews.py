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
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from itertools import chain
from hospital.utility import render_to_pdf

def receptionist_dashboard(request):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Receptionist':
            today = date.today()
            data = Appointment.objects.filter(app_date=today)
            return render(request, 'hospital/receptionist/dashboard.html', {'data': data})
        else:
            return redirect('/')
    else:
        return redirect('/')

def receptionist_appointments(request):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Receptionist':
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
                return render(request, 'hospital/receptionist/appointment_list.html', {'app_list': app_list, 'show_date': get_date, 'doctor': doctor})

            else:
                show_date = date.today().strftime("%Y-%m-%d")
                doctor = Profile.objects.filter(user_type='Doctor')
                app_list = Appointment.objects.filter(app_date=date.today()).all()
                return render(request, 'hospital/receptionist/appointment_list.html', {'app_list': app_list, 'show_date': show_date, 'doctor': doctor})
        else:
            return redirect('/')
    else:
        return redirect('/')

def receptionist_appointment_confirm(request, id):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Receptionist':
            data = Appointment.objects.get(pk=id)
            data.appointment_status = True
            messages.success(request, f'Appointment successfull confirm for <strong>"{data.full_name}"</strong>.')
            data.save()
            return redirect('/receptionist/appointment_list/')
        else:
            return redirect('/')
    else:
        return redirect('/')

def receptionist_patients(request):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Receptionist':
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

                    doctors = Profile.objects.filter(user_type='Doctor')    
                    return render(request, 'hospital/receptionist/patient_list.html', {'emp': emp, 'doctor': doctors})


                else:
                    emp = Profile.objects.filter(user_type='Patient')
                    doctors = Profile.objects.filter(user_type='Doctor')
                    return render(request, 'hospital/receptionist/patient_list.html', {'emp': emp, 'doctor': doctors})    
            else:
                emp = Profile.objects.filter(user_type='Patient')
                doctors = Profile.objects.filter(user_type='Doctor')
                return render(request, 'hospital/receptionist/patient_list.html', {'emp': emp, 'doctor': doctors})
        else:
            return redirect('/')
    else:
        return redirect('/')

def receptionist_view_record(request, user_info):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Receptionist':
            patient_data = User.objects.filter(username=user_info)
            # records = Medical_Record.objects.values('user', 'date').filter(user=user_info, doctor_name=doctorname)
            records = Medical_Record.objects.values('user', 'date').filter(user=user_info).annotate(Count('id')).order_by()
            # records = Medical_Record.objects.raw('SELECT COUNT (*), date from hospital_medical_record GROUP BY date')
            return render(request, 'hospital/receptionist/viewrecord.html', {'patient_data': patient_data, 'records': records})
        else:
            return redirect('/')
    else:
        return redirect('/')

def receptionist_view_prescription(request, user_info, date):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Receptionist':
            rec_date = datetime.datetime.strptime(date, "%m-%d-%Y").date()
            user_detail = User.objects.values('first_name', 'last_name').filter(username=user_info)
            get_doc_name = Medical_Record.objects.values('doctor_name').filter(user=user_info).annotate(Count('id')).order_by()
            records = Medical_Record.objects.filter(user = user_info, date=rec_date)
            # doc_name = None
            for i in get_doc_name:
                doc_name = i['doctor_name']

            data = {
                'date' : date,
                'records': records,
                'doc_name': doc_name,
                'user_data' : user_detail,
            }
            
            pdf = render_to_pdf('hospital/receptionist/showrecords.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            return redirect('/')
    else:
        return redirect('/')

def payment_confirmation(request, id):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Receptionist':
            data = Appointment.objects.get(pk=id)
            data.is_pay = True
            data.save()
            return redirect('/receptionist/dashboard/')
        else:
            return redirect('/')
    else:
        return redirect('/')

def new_patient(request):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Receptionist':
            if request.method == 'POST':
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                username = request.POST['username']
                passwd = request.POST['passwd']
                mobile = request.POST['mob']
                email = request.POST['email']
                address = request.POST['address']
                gender = request.POST['gender']
                age = request.POST['age']
                blood_group = request.POST['blood_group']
                enc_pass = make_password(passwd)
                user_data = User(first_name=first_name, last_name=last_name, username=username, password=enc_pass, email=email)
                user_data.save()
                user_id = user_data.id
                profile_data = Profile(user_type='Patient', address=address, mobile=mobile, blood_group=blood_group, gender=gender, age=age, user_id= user_id)
                profile_data.save()
                messages.success(request, f'User <strong>{first_name} {last_name}</strong> is successfully created.')
                return redirect('/receptionist/new_patient/')
            else:
                return render(request, 'hospital/receptionist/new_patient.html')

        else:
            return redirect('/')
    else:
            return redirect('/')

def new_appointment(request):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Receptionist':
            if request.method == 'POST':
                patient_username = request.POST['username']
                doc_username = request.POST['doc_username']
                app_date = datetime.datetime.strptime(request.POST['date'], "%Y-%m-%d").date()
                patient_data = User.objects.filter(username=patient_username)
                doctor_data = User.objects.filter(username=doc_username)
                today = date.today()
                if app_date > today:
                    for i in patient_data:
                        full_name = i.first_name +" "+ i.last_name
                        mobile = i.profile.mobile
                    
                    for i in doctor_data:
                        doctor_name = i.first_name + " " + i.last_name
                        dep = i.profile.department                
                    app_count = Appointment.objects.filter(doctor_name=doctor_name, app_date=app_date).count()
                    if app_count < 10:
                        app_no = app_count + 1
                        check_data = Appointment.objects.filter(user=patient_username, doctor_name=doctor_name, app_date=app_date)
                        if check_data:
                            messages.warning(request, f'Appointment is already created for <strong>{full_name}</strong> on date <strong>{app_date}</strong>.')
                            
                        else:
                            new_app = Appointment(user=patient_username, app_date=app_date, doctor_name=doctor_name, department=dep, book_date=today, full_name=full_name, mobile=mobile, appointment_no=app_no)
                            new_app.save()
                            messages.success(request, f'New appointment is created for <strong>{full_name}</strong> on date <strong>{app_date}</strong>.')
                            
                    else:
                        messages.success(request, f'Appointment is not available on date {app_date}, please select another date for appointment.')
                else:
                    messages.warning(request, f'New appointment date must be greater than today.')
                return redirect('/receptionist/patient_list/')
        else:
            return redirect('/')
    else:
        return redirect('/')

def receptionist_profile(request):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Receptionist':
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
                    return redirect('/receptionist/profile/')
                else:
                    return render(request, 'hospital/receptionist/profile.html', {'profile_form': profile_form, 'add_profile_form': add_profile_form })
            
            else:
                return render(request, 'hospital/receptionist/profile.html',{'profile_form': profile_form, 'add_profile_form': add_profile_form })
        else:
            return redirect('/')
    else:
        return redirect('/')

def receptionist_password(request):
    if request.user.is_authenticated:
        if request.session['user_type'] == 'Receptionist':
            if request.method == 'POST':
                form = ChangePasswordForm(user = request.user, data = request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                    messages.success(request, 'Password is successfully changed.')
                    return redirect('/receptionist/passwordchange/')
                
                else:
                    return render(request, 'hospital/receptionist/passwordchange.html', {'form': form})        
            
            else:
                form = ChangePasswordForm(user = request.user)
                return render(request, 'hospital/receptionist/passwordchange.html', {'form': form})
        else:
            return redirect('/')
    else:
        return redirect('/')

def receptionist_logout(request):
    logout(request)
    return redirect('/')