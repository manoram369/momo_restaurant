from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import *
from django.contrib.auth.decorators import login_required
import re
from django.contrib.auth import authenticate ,login ,logout
from django.contrib.auth.forms import PasswordChangeForm

import logging
logger=logging.getLogger("django")
# Create your views here.
def index(request):
    momo=None
    try:
    

        category=Category.objects.all()
        category_id=request.GET.get('category')
    
        if category_id=="all":
            momo=Momo.objects.all()
        elif category_id:
            momo=Momo.objects.filter(category=category_id)
        else:
            momo=Momo.objects.all()
    except Exception as e:
        logger.error(e,exc_info=True)
    context={
        'category':category,
        'momo':momo
    }
    
    return render(request,"core/index.html",context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        user_message = request.POST.get("message")

        Contact.objects.create(
            name=name,
            phone=phone,
            email=email,
            subject=subject,
            message=user_message
        )
        messages.success(request, f"Hello {name}, your form submitted successfully")
        return redirect("contact")
    return render(request, "core/contact.html")


@login_required(login_url='log_in')
def menu(request):
    category=Category.objects.all()
    return render(request,"core/menu.html",{'category':category})
@login_required(login_url='log_in') 
def services(request):
    return render(request,"core/services.html")
def testemonial(request):
    return render(request,"core/testemonial.html")
def about(request):
    return render(request,"core/about.html")
def Register(request):
    if request.method =='POST':
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']

        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.error(request, "user name is already exist")
                return redirect ('register')
            
            if not re.search(r"[A-Z]",password):
                messages.error(request,"yoour password must be contain at least one upper case")
                return redirect('register')
            if not re.search(r"\d",password):
                messages.error(request,"yoour password must be contain at least one digit")
                return redirect('register')
            if not re.search(r"\W",password):
                messages.error(request,"your password must be contain at least one special character")
                return redirect('register')
            if not re.search(r"\w",password):
                messages.error(request,"your password must be contain at least one lower case")
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.error(request, "user email is already exist")
                return redirect ('register')
            try:
                validate_password(password)
                User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                messages.success(request,"your account is successfully register")
                return redirect('register')
            except ValidationError as e:
                for i in e.messages:
                    messages.error(request ,i )
                    return redirect('register')
        else:
            messages.error(request, "password does not match !!")
            return redirect('register')

    return render(request,"accounts/register.html")
def log_in(request):
    if request.method =='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        remember_me=request.POST.get('remember_me')

        if not User.objects.filter(username=username).exists():
            messages.error(request,"username is not register yet")
            return redirect ('log_in')
        user=authenticate(username=username,password=password)
        # print("user : ",user)
        if user is not None:
            login(request,user)
            if remember_me:
                request.session.set_expiry(1200000)
            else:
                request.session.set_expiry(0)

            next=request.POST.get("next","")
            # print("yes") if next else print ("no")
            return redirect(next if next else "index")
        else:
            messages.error(request,"password invalid")
            return redirect('log_in')
        
    next=request.GET.get("next","")
    return render(request,"accounts/login.html",{"next":next})


def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def password_change(request):
    form=PasswordChangeForm(user=request.user)
    if request.method =='POST':
        form=PasswordChangeForm(user=request.user , data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("log_in")

    return render(request, 'accounts/password_change.html',{'form':form})
