from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Graphical
import time
import datetime
import os
import random
from django.contrib.auth.decorators import login_required
from GUAS.settings import MEDIA_ROOT, MEDIA_URL


# Create your views here.


def index(request):

    # print(os.listdir(r"./static/passimages"))
    if request.method == 'POST':
        Images = request.POST.getlist('image')
        print(Images)
    images = list()
    fl = os.listdir(r"./static/passimages")
    while len(images) < 5:
        x = random.choice(fl)
        if x not in images:
            images.append(x)
    random.shuffle(images)
    return render(request, 'home.html', {"images": images})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        Images = request.POST.getlist('image')
        print(Images)
        # get image avaible in our backend server
        avail_img = os.listdir(r"./static/passimages")
        time_stamp = [int(str(x).split('.')[0]) for x in Images]
        file_name = [str(x).split("/")[-1].replace('"', '')
                     for x in Images]  # get the input filename
        for l in file_name:  # cheak if the user request files are in server or not
            if l not in avail_img:
                messages.info(
                    request, 'The selected object is not availble in server')
                return redirect(signup)
        maped = dict(zip(time_stamp, file_name))
        print(maped)
        time_sort = dict(sorted(maped.items()))
        img_pass = "".join([maped[i] for i in time_sort])
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Used')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password+img_pass)
                user.save()
                messages.info(request, 'Account Created Succesfully')
                # login the user and redireting to setting of profile
                user_login = auth.authenticate(
                    username=username, password=password+img_pass)
                auth.login(request, user_login)
                user_model = User.objects.get(username=username)
                new_profile = Graphical.objects.create(
                    user=user_model, img1=file_name[0], img2=file_name[1], img3=file_name[2])
                new_profile.save()
                return render(request, "result.html", {"usern": user_model, "passw": password, "images": file_name})
        else:
            messages.info(request, 'Password are not same')
            return redirect('signup')
    images = list()
    fl = os.listdir(r"./static/passimages")
    while len(images) < 5:
        x = random.choice(fl)
        if x not in images:
            images.append(x)
    random.shuffle(images)
    return render(request, 'signup.html', {"images": images})


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


def signin(request):
    show = True
    if request.method == 'POST':
        username = request.POST['username']
        if not (request.POST.get('password')):
            user_dtl = User.objects.filter(username=username)
            if not (user_dtl):
                messages.info(request, "Username not Found")
                return redirect('signin')
            user_dtl = User.objects.get(username=username)
            graps = Graphical.objects.get(user=user_dtl)
            img = [graps.img1, graps.img2, graps.img3]
            Locals = os.listdir(r"./static/passimages")
            Images = img
            while len(Images) < 5:
                x = random.choice(Locals)
                if x not in Images:
                    Images.append(x)
            random.shuffle(Images)
            return render(request, "signin.html", {"images": Images, "godwatch": username, "bol": False})
        password = request.POST['password']
        Images = request.POST.getlist('image')
        print(Images)
        # get image avaible in our backend server
        avail_img = os.listdir(r"./static/passimages")
        time_stamp = [int(str(x).split('.')[0]) for x in Images]
        file_name = [str(x).split("/")[-1].replace('"', '')
                     for x in Images]  # get the input filename
        for l in file_name:  # cheak if the user request files are in server or not
            if l not in avail_img:
                messages.info(
                    request, 'The selected object is not availble in server')
                return redirect(signup)
        maped = dict(zip(time_stamp, file_name))
        print(maped)
        time_sort = dict(sorted(maped.items()))
        img_pass = "".join([maped[i] for i in time_sort])
        password = password+img_pass
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html', {"bol": show})
