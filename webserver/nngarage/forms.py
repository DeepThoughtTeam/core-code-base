from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import NetDescription
from models import Profile


# Database-driven app needs the ModelForm
# The user form that connect the backend model with the front end input
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

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


# The ModelForm for user to edit their own profile
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {"password1", "password2", "first_name", "last_name", "image"}
        # Placeholder for widgets
        widgets = {'password1': forms.PasswordInput(), 'password2': forms.PasswordInput(), 'image': forms.FileInput()}

    # Same as the the phase for user creation, validate the password only.
    def clean(self):
        cleaned_data = super(ProfileEditForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match.")

        return cleaned_data

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1 == "":
            raise forms.ValidationError("Password is empty.")

        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')

        if password2 == "":
            raise forms.ValidationError("Confirm password is empty.")

        return password2


class NetDescUploadForm(forms.ModelForm):
    class Meta:
        model = NetDescription
        fields = {"name", "file_ins"}

    def clean(self):
        cleaned_data = super(NetDescUploadForm, self).clean()
        return cleaned_data


    def clean_name(self):
        name = self.cleaned_data.get("name")

        if NetDescription.objects.filter(name__exact=name):
            raise forms.ValidationError("Net Description's name is already taken.")

        return name
