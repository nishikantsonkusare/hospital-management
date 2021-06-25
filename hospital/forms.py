from django.contrib.auth.models import User
from hospital.models import Profile, Appointment
from django.forms import ModelForm
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from datetime import date, timedelta

class NewUserForm(ModelForm):
    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'email', 'username', 'password']

        help_texts ={
            'username': None,
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':'First Name', 'class': 'form-control', 'autocomplete': 'off'}),
            'last_name' : forms.TextInput(attrs={'placeholder':'Last Name', 'class': 'form-control', 'autocomplete': 'off'}),
            'email' : forms.EmailInput(attrs={'placeholder':'Email Address', 'class': 'form-control', 'autocomplete': 'off'}),
            'username' : forms.TextInput(attrs={'placeholder':'Username', 'class': 'form-control', 'autocomplete': 'off'}),
            'password' : forms.PasswordInput(attrs={'placeholder':'Password', 'class': 'form-control', 'autocomplete': 'off'}),
        }


    def clean(self):
        super(NewUserForm, self).clean()

        first_name = self.cleaned_data.get('first_name', None)
        last_name = self.cleaned_data.get('last_name', None)
        email = self.cleaned_data.get('email', None)
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not first_name:
            self.add_error('first_name', 'Please enter first name.')
        if not last_name:
            self.add_error('last_name', 'Please enter last name.')
        if not email:
            self.add_error('email', 'Please enter email address.')
        if len(username) < 6 :
            self.add_error('username', 'Username must be greater than 6 character.')
        if len(password) < 6 :
            self.add_error('password', 'Password must be greater than 6 character.')
        if len(password) > 20 :
            self.add_error('password', 'Username must be less than 20 character.')

        return self.cleaned_data


class LoginForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput({'placeholder':'Username', 'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput({'placeholder':'Password', 'class': 'form-control', 'autocomplete': 'off'}))

    def clean(self):
        super(LoginForm, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Please enter valid username and password.')

        return self.cleaned_data


class ProfileForm(ModelForm):
    
    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':'First Name', 'class': 'form-control', 'autocomplete': 'off'}),
            'last_name' : forms.TextInput(attrs={'placeholder':'Last Name', 'class': 'form-control', 'autocomplete': 'off'}),
            'email' : forms.EmailInput(attrs={'placeholder':'Email Address', 'class': 'form-control', 'autocomplete': 'off'}),
        }


    def clean(self):

        super(ProfileForm, self).clean()

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')

        if not first_name:
            self.add_error('first_name', 'Please enter first name.')
        if not last_name:
            self.add_error('last_name', 'Please enter first name.')
        if not email:
            self.add_error('email', 'Please enter email address.')

        return self.cleaned_data


class AdditionalProfileForm(ModelForm):
    class Meta:
        model = Profile

        fields = ['address', 'mobile', 'blood_group', 'age', 'profile_pic']

        widgets = {
            'mobile' : forms.TextInput(attrs={'placeholder':'Mobile Number', 'class': 'form-control', 'autocomplete': 'off'}),
            'address' : forms.TextInput(attrs={'rows': '3', 'placeholder':'Address', 'class': 'form-control', 'autocomplete': 'off'}),
            'blood_group' : forms.Select(attrs={'class': 'form-select'}),
            'age' : forms.NumberInput(attrs={'placeholder':'Age', 'class': 'form-control', 'autocomplete': 'off'}),
            'profile_pic' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        super(AdditionalProfileForm, self).clean()

        mobile = self.cleaned_data.get('mobile')
        bod = self.cleaned_data.get('date_of_birth')
        pic = self.cleaned_data.get('profile_pic')

        if pic:
            if pic.size > 5242880 :
                self.add_error('profile_pic', 'Profile image size must be less than 5 MB.')

        if mobile is None:
            self.add_error('mobile', 'Please enter mobile number.')

        return self.cleaned_data

class AppointmentForm(forms.Form):
    
    app_date = forms.DateField(widget=forms.TextInput(attrs={'placeholder':'MM/DD/YYYY', 'class': 'form-control', 'id': 'datepicker1', 'autocomplete': 'off'}))
    
    def clean(self):
        super(AppointmentForm, self).clean()

        appointment_date = self.cleaned_data.get('app_date')

        if appointment_date < date.today() + timedelta(days=1):
            self.add_error('app_date', 'Please select valid date for appointment.')
        
        if appointment_date > date.today() + timedelta(days=15):
            self.add_error('app_date', 'Appointment date must be between 15 days.')
        
        return self.cleaned_data

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label = 'Old Password',
        strip = False,
        widget = forms.PasswordInput(attrs={ 'placeholder': 'Enter Old Password', 'class' : 'form-control', 'autocomplete': 'off'})
    )

    new_password1 = forms.CharField(
        label = 'New Password',
        strip = False,
        widget = forms.PasswordInput(attrs={ 'placeholder': 'Enter New Password', 'class' : 'form-control', 'autocomplete': 'off'})
    )

    new_password2 = forms.CharField(
        label = 'New Password Again',
        strip = False,
        widget = forms.PasswordInput(attrs={ 'placeholder': 'Enter New Password Again', 'class' : 'form-control', 'autocomplete': 'off'})
    )

class DoctorProfileForm(ModelForm):
    class Meta:
        model = Profile

        fields = ['address', 'mobile', 'blood_group', 'age', 'profile_pic', 'department']

        widgets = {
            'department' : forms.TextInput(attrs={'placeholder':'Department Name', 'class': 'form-control', 'autocomplete': 'off'}),
            'mobile' : forms.TextInput(attrs={'placeholder':'Mobile Number', 'class': 'form-control', 'autocomplete': 'off'}),
            'address' : forms.TextInput(attrs={'rows': '3', 'placeholder':'Address', 'class': 'form-control', 'autocomplete': 'off'}),
            'blood_group' : forms.Select(attrs={'class': 'form-select'}),
            'age' : forms.NumberInput(attrs={'placeholder':'Age', 'class': 'form-control', 'autocomplete': 'off'}),
            'profile_pic' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        super(DoctorProfileForm, self).clean()

        mobile = self.cleaned_data.get('mobile')
        bod = self.cleaned_data.get('date_of_birth')
        pic = self.cleaned_data.get('profile_pic')
        dept = self.cleaned_data.get('department')

        if not dept:
            self.add_error('department', 'Please entered valid department name')

        if pic:
            if pic.size > 5242880 :
                self.add_error('profile_pic', 'Profile image size must be less than 5 MB.')

        if mobile is None:
            self.add_error('mobile', 'Please enter mobile number.')

        return self.cleaned_data
