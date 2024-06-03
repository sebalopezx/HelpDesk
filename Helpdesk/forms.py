from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class TicketAdminForm(forms.ModelForm):
    opening_agent = forms.ModelMultipleChoiceField(queryset=Profile.objects.all(), widget=FilteredSelectMultiple('opening_agent', False), label='Agente apertura')
    closure_agent = forms.ModelMultipleChoiceField(queryset=Profile.objects.all(), widget=FilteredSelectMultiple('closure_agent', False), label='Agente cierre')

    class Meta:
        model = Ticket
        fields = '__all__'
        

# class CustomUserCreationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=False)
#     last_name = forms.CharField(max_length=30, required=False)
#     email = forms.EmailField(required=False)
#     is_active = forms.BooleanField(required=False)
#     is_staff = forms.BooleanField(required=False)
#     is_superuser = forms.BooleanField(required=False)

#     class Meta:
#         model = User
#         fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # fields = UserCreationForm.Meta.fields
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Password',
            'password2': 'Confirmación Password',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email'
        }

class CustomProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['rut', 'phone']

class CustomUserAndProfileForm(forms.ModelForm):
    # user_form = CustomUserCreationForm()
    # profile_form = CustomProfileCreationForm()

    class Meta:
        model = User
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_form = CustomUserCreationForm(*args, **kwargs)
        self.profile_form = CustomProfileCreationForm(*args, **kwargs)
        # Update fields to include fields from both forms
        self.fields.update(self.user_form.fields)
        self.fields.update(self.profile_form.fields)
        # Add initial data for profile form fields if present
        self.initial.update(self.user_form.initial)
        self.initial.update(self.profile_form.initial)
        

    def is_valid(self):
        return self.user_form.is_valid() and self.profile_form.is_valid()
    
    def save(self, commit=True):
        user = self.user_form.save(commit=False)
        if commit:
            user.save()
        profile = self.profile_form.save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return user
    

class OpeningTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('customer', 'issue', 'priority', 'type', 'observation')

    def __init__(self, *args, **kwargs):
        super(OpeningTicketForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = Profile.objects.filter(user__is_staff=False)
        print(self.fields['customer'].queryset)


class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('issue', 'priority', 'type', 'status', 'observation', 'solution')
    
