from django import forms
from django.contrib.auth import get_user_model

from accounts.models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Enter Your Password"
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password"
    }))

    class Meta:
        model = Account
        fields = ["first_name", 'last_name',
                  "email", "password", "phone_number"]
        labels = {
            "username": " Your Name",
            "first_name": "Your First Name",
            "last_name": "Your Last name",
            "email": "Your Email Address",
            "phone_number": "Your Phone Number"
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Enter Your First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter Your Last Name"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Enter Your Phone Number"
        self.fields["password"].widget.attrs["placeholder"] = "Enter Your Password"
        self.fields["confirm_password"].widget.attrs["placeholder"] = "Confirm Your Password"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(" Password doesn't match!")


# class LoginForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={
#         "placeholder": "Enter Your Password"
#     }))

#     class Meta:
#         model = Account
#         fields = ["email", "password"]
