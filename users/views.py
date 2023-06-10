from django.shortcuts import render,HttpResponse,redirect

from .forms import CreateUserForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .decorators import *
from django.core.mail import send_mail
import random

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

from django.contrib.auth.tokens import default_token_generator
import secrets
import random
import string
import time
import smtplib
import pyotp
from email.mime.text import MIMEText
from django.core.exceptions import ObjectDoesNotExist

def login_app(request):
    return HttpResponse('login')



@unauthenticated_user
def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # Check if an Employee_profile object with the given email already exists
            email = form.cleaned_data.get('email')
            employee_profile = user_profile.objects.filter(email=email).first()
            if not employee_profile:
                employee_profile = user_profile.objects.create(
                    user=user,
                    name=user.username,
                    email=email,
                )

            current_site = get_current_site(request)
            mail_subject = 'An account has been'
            message = render_to_string('template_activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail = email
            print(send_mail)
            email = EmailMessage(mail_subject, message, to=[send_mail])
            email.send()
            messages.success(request, 'Check your email for Active acount')
            return redirect('loginpage')
        else:
            messages.error(request, 'Email or phone already exists.')
    else:
        form = CreateUserForm()

    return render(
        request=request,
        template_name="register.html",
        context={"form": form}
    )


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.info(request, 'Your Account is activated now')
        return redirect('loginpage')
    

# Login Process Started Here
@unauthenticated_user


def loginpage(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                messages.info(request, 'You have no account')
                return redirect('loginpage')

            if not user.is_active:
                messages.info(request, 'Your account is not activated check your Mail')
                return redirect('loginpage')
            
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                messages.success(request,'Successfully Logged In')
                login(request,user)
                # return redirect('upload')
                
            for g in request.user.groups.all():
                if g.name == 'normaluser':
                    if request.user.user_profile: 
                        return redirect('mainpage')
                    else:
                        return redirect('mainpage')
                
                # elif g.name == 'hr':
                #     return redirect('hrdashboard')
            else:
                # print('Username or password not found')
                messages.error(request,'User name or password not found')

    except:
        return redirect('loginpage')
    context = {}
    return render(request, 'login.html',context)



def logoutuser(request):
    logout(request)
    return redirect('loginpage')
