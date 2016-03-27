from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import Task


# Database-driven app needs the ModelForm
# The user form that connect the backend model with the front end input
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'FirstName',
            'last_name': 'LastName',
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:  # raise error to user if necessary
            raise forms.ValidationError("Password did not match.")

        # Passed
        return cleaned_data

    # Prevent duplicate username in DB
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        return username

    # Prevent duplicate email address in DB
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.")

        return email


