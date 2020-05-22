from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()
class ContactForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
                attrs={
                    'class': "form-control",
                    "placeholder":"Your full name"
                }
            )
        )
    email = forms.EmailField(
        widget=forms.EmailInput(
                attrs={
                    'class': "form-control",
                    "placeholder":"Your email"
                }
            )
        )
    content = forms.CharField(
        widget=forms.TextInput(
                attrs={
                    'class': "form-control",
                    "placeholder":"Your message"
                }
            )
        )
    def clean_fullname(self):
        fullname = self.cleaned_data.get("fullname")
        if len(fullname) > 30 :
            raise forms.ValidationError("Full name must be in 30 charecters")
        return fullname

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  # if you haven't use this widget, password will get displayed 

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password",widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username = username)
        if qs.exists():
            raise forms.ValidationError("User already exist")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email = email)
        if qs.exists():
            raise forms.ValidationError("email already exist")
        return ename

    def clean(self):
        pass1 = self.cleaned_data.get("password")
        pass2 = self.cleaned_data.get("password2")
        if pass1 != pass2 :
            raise forms.ValidationError("Password must be same")
        return self.cleaned_data
