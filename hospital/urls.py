"""hospital_mgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from hospital.views import views, patientviews, doctorviews, adminview, receptionistviews

urlpatterns = [
    path('', views.home, name='Home'),
    path('registration/', views.register, name='registration'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # This is urls for patient modules
    path('patient/dashboard/', patientviews.patient_dashboard, name='patient_dashboard'),
    path('patient/profile/', patientviews.patient_profile, name='patient_profile'),
    path('patient/appointment/', patientviews.patient_appointment, name='patient_appointment'),
    path('patient/passwordchange/', patientviews.patient_password, name='patient_password_change'),
    path('patient/prescription/user=<str:user_info>/doctor_name=<str:doctor_name>/date=<str:date>', patientviews.view_prescription, name='view_prescription'),
    path('patient/logout/', patientviews.patient_logout, name='patient_logout'),

    # This is urls for doctor modules
    path('doctor/dashboard/', doctorviews.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/appointment_list/', doctorviews.doctor_appointments, name='doctor_appointment_list'),
    path('doctor/patient_list/', doctorviews.doctor_patients, name='doctor_patient_list'),
    path('doctor/prescription/appointment_id=<int:id>', doctorviews.doctor_prescription, name='doctor_prescription'),
    path('doctor/viewrecord/patient=<str:user_info>', doctorviews.view_record, name='view_record'),
    path('doctor/showprescription/patient=<str:user_info>/date=<str:date>', doctorviews.view_prescription, name='view_prescription'),
    path('doctor/profile/', doctorviews.doctor_profile, name='doctor_profile'),
    path('doctor/passwordchange/', doctorviews.doctor_password, name='doctor_password_change'),
    path('doctor/appointment/conform/<int:id>', doctorviews.appointment_confirm, name='appointment_confirm'),
    path('doctor/logout/', doctorviews.doctor_logout, name='doctor_logout'),

    # Admin Modules Url
    path('admin/dashboard/', adminview.admin_dashboard, name='admin_dashboard'),
    path('admin/employee_list/', adminview.admin_employee, name='admin_emmployee_list'),
    path('admin/appointment_list/', adminview.admin_appointments, name='admin_appointment'),
    path('admin/appointment/conform/<int:id>', adminview.appointment_confirm, name='admin_appointment_confirm'),
    path('admin/patient_list/', adminview.admin_patients, name='admin_patient'),
    path('admin/pending_users/', adminview.admin_pending_users, name='admin_pending_user'),
    path('admin/approved_users/<int:id>', adminview.admin_user_approved, name='admin_approved_user'),
    path('admin/profile/', adminview.admin_profile, name='admin_profile'),
    path('admin/passwordchange/', adminview.admin_password, name='admin_password'),
    path('admin/logout/', adminview.doctor_logout, name='admin_logout'),

    # Receptionist Modules Url
    path('receptionist/dashboard/', receptionistviews.receptionist_dashboard, name='receptionist_dashboard'),
    path('receptionist/appointment_list/', receptionistviews.receptionist_appointments, name='receptionist_appointments'),
    path('receptionist/appointment/conform/<int:id>', receptionistviews.receptionist_appointment_confirm, name='receptionist_appointment_confirm'),
    path('receptionist/new_patient/', receptionistviews.new_patient, name='new_patient'),
    path('receptionist/patient_list/', receptionistviews.receptionist_patients, name='receptionist_patients'),
    path('receptionist/new_appointment/', receptionistviews.new_appointment, name='new_appointment'),
    path('receptionist/viewrecord/patient=<str:user_info>', receptionistviews.receptionist_view_record, name='receptionist_view_record'),
    path('receptionist/showprescription/patient=<str:user_info>/date=<str:date>', receptionistviews.receptionist_view_prescription, name='receptionist_view_prescription'),
    path('receptionist/payment_confirmation/appointment_id=<int:id>', receptionistviews.payment_confirmation, name='payment_confirmation'),
    path('receptionist/profile/', receptionistviews.receptionist_profile, name='receptionist_profile'),
    path('receptionist/passwordchange/', receptionistviews.receptionist_password, name='receptionist_password'),
    path('receptionist/logout/', receptionistviews.receptionist_logout, name='receptionist_logout'),
]

