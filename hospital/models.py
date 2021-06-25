from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
# Create your models here.

BLOOD_GROUP_CHOICE = (
    (1, _("A+")),
    (2, _("B+")),
    (3, _("O+")),
    (4, _("AB+")),
    (5, _("A-")),
    (6, _("B-")),
    (7, _("O-")),
    (8, _("AB-")),
)

GENDER_CHOICE = (
    (1, _("Male")),
    (2,_("Female")),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=15, null=True,blank=False)
    address = models.CharField(max_length=256, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^[6-9]\d{9}$', message="Please enter valid mobile number.")
    mobile = models.CharField(validators=[phone_regex], max_length=10, blank=True)
    blood_group = models.IntegerField(choices=BLOOD_GROUP_CHOICE, default=1)
    gender = models.IntegerField(choices=GENDER_CHOICE, default=1)
    age = models.PositiveIntegerField(default=0)
    department = models.CharField(max_length=50, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profiles', blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    # id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.CharField(max_length=256, null=False, blank=False)
    full_name = models.CharField(max_length=256, null=False, blank=False, default='')
    mobile = models.CharField(max_length=10, null=False, blank=False, default='')
    app_date = models.DateField(null=False, blank=False)
    book_date = models.DateField(null=False, blank=False, auto_now=True)
    doctor_name = models.CharField(max_length=256, null=False, blank=False)
    department = models.CharField(max_length=100, null=False, blank=False)
    fees = models.PositiveIntegerField(null=False, blank=False, default=500)
    is_pay = models.BooleanField(default=False)
    appointment_no = models.PositiveIntegerField(null=False, blank=False, default=0)
    appointment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user

class Medical_Record(models.Model):
    user = models.CharField(max_length=256, null=False, blank=False)
    doctor_name = models.CharField(max_length=256, null=False, blank=False)
    department = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateField()
    prescription = models.CharField(max_length=1024, null=False, blank=False)
    days = models.PositiveIntegerField(default=3)

    def __str__(self):
        return self.user
