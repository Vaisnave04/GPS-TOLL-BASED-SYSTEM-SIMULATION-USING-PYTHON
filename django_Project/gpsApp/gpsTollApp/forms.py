# myapp/forms.py
from django import forms
from .models import vehiclecategory
from .models import userprofile
from .models import gpstollapptrip
from django.contrib.auth.forms import PasswordChangeForm

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}))

    class Meta:
        model = userprofile  # Replace with your User model if different
        fields = ['old_password', 'new_password1', 'new_password2']

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = userprofile
        
        fields = ['user_id', 'first_name', 'last_name', 'sex', 'email', 'password', 'address', 'super_user','id']
        widgets = {
            'password': forms.PasswordInput(),
        }

class VehicleCategoryForm(forms.ModelForm):
    class Meta:
        model = vehiclecategory
        fields = ['id', 'category_id', 'vehicle_type', 'toll_amount']
        
class TripForm(forms.ModelForm):
    class Meta:
        model = gpstollapptrip
        fields = ['trip_id', 'source', 'destination', 'no_tollscrossed', 'total_amount', 'payment_status', 'trip_date', 'vehicle_regno', 'Applicant_name', 'vehicle_catid', 'validity_from', 'validity_to', 'costof_pass']
       

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class UserForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)