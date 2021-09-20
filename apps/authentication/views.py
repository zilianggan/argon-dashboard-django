# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from .forms import LoginForm, SignUpForm
from .models import *

def register_user(request):
    msg = None
    success = False
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        username = request.POST['username']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        email = request.POST['email']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        dob = request.POST['dob']
       
        if password == confirm_password:
            if not User.objects.filter(username = username).exists() and not User.objects.filter(email = email).exists():
                user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name,last_name=last_name,dob=dob)
                user.save()
                success=True
            return redirect("/login/")
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.filter(username=username)
            if user:
                user = user[0]
                # user = authenticate(username=username)
                checkPassword = check_password(password,user.password)
                if user is not None and checkPassword:
                    login(request, user)
                    return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})