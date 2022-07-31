from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm
from .models import Account

# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            password = form.cleaned_data["password"]
            phone_number = form.cleaned_data["phone_number"]
            confirm_password = form.cleaned_data["confirm_password"]
            email = form.cleaned_data["email"]
            username = email.split('@')[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                               email=email, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, "Registration Successful")
            return redirect('register')
    else:
        form = RegistrationForm()
        context = {
            "form": form,
        }
        return render(request, "accounts/register.html", context)


def login(request):
    if request.method == "POST":
        print(request.POST)
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Welcome")
            return redirect('home')

        # user = Account.objects.get(email=email)
        # if user.password == password:

        else:
            messages.error(request, "Invalid Login Credentials")
            return redirect('login')
    else:

        return render(request, "accounts/login.html")


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect('login')
