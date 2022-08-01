from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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

            # send Verification
            current_site = get_current_site(request)
            mail_subject = " Please Activate your Account"
            message = render_to_string("accounts/account_verification_email.html", {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),

            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])

            send_email.send()

            # messages.success(request, "Thank You for registering with us. We have a sent you a mail []!")
            return redirect('/accounts/login/?command=verification&email=' + email)
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
            messages.success(request, "You're Logged In!")
            return redirect('dashboard')

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


def activate(request, uidb64, token):
    try:
        user_pk = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=user_pk)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None:
        user.is_active = True
        user.save()
        messages.success(
            request, "Congratulations! Your account is activated.")
        return redirect('login')

    else:
        messages.error(request, "Invalid Activation Link")
        return redirect('register')


# @login_required(login_url='login')
def dashboard(request):
    return render(request, "accounts/dashboard.html")
