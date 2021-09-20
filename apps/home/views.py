# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
from django.template import loader
from django.urls import reverse
from .models import *
from .forms import *
from django.conf import settings
from ..authentication.forms import *
from ..authentication.models import *
from django.contrib import messages

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    
@login_required
def editProfile(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        dob = request.POST['dob']
        dob = datetime.datetime.strptime(dob, '%Y-%m-%d')

        exist = User.objects.exclude(id=request.user.id).filter(email = email).exists()
        
        if user is not None and not exist:
            user.email=email
            user.first_name = first_name
            user.last_name = last_name
            user.dob = dob
            user.save()
            messages.success(request,"Successfully edit profile!")
        else:
            messages.error(request,"Email has been used!")
    context = {
        'user': user,
    }
    return render(request, 'home/profile.html',context)

@login_required
def uploadProfilePic(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile-picture')
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
        file_extension = profile_picture.name.split('.')[-1].lower()
        if profile_picture and file_extension in allowed_extensions:
            exist = UserProfile.objects.filter(user=user)
            if exist:
                user_profile = request.user.userprofile
                user_profile.profile_picture.delete(save=False)
                user_profile.profile_picture = profile_picture
            else:
                user_profile = UserProfile.objects.create(user=request.user, profile_picture=profile_picture)
            request.user.userprofile.save()
            messages.success(request,"Successfully upload profile picture!")
        else:
            messages.error(request,"Please upload png, jpg or jpeg picture!")
    return render(request, 'home/profile.html')


def createClub(request):
    msg = None
    success = False
    user = User.objects.get(id=request.user.id)
    universities = University.objects.all().order_by('name')
    sports = Sport.objects.all().order_by('name')
    
    if request.method == "POST":
        new_club = Club(
            name = request.POST['name'],
            description = request.POST['description'],
            sport = Sport.objects.get(id=request.POST['sport']),
            university = University.objects.get(id=request.POST['university']),
        )
        new_club.save()

        newClubMember = ClubMember(
            club = new_club,
            member = user,
            position = 'President'
        )
        newClubMember.save()

        images = request.FILES.getlist('image')
        for img in images:
            ClubImage.objects.create(club=new_club,image=img)

        msg = 'Successfully created club'
        context = {
            'msg' : msg,
            'success':success,
        }
        return render(request, "home/index.html", context)
    
    form = ImageForm()
    context = {
        'form':form,
        'universities': universities,
        'sports' : sports,
    }
    return render(request, "home/create_club.html", context)

def clubList(request):
    clubs = Club.objects.all().order_by('name')
    club_list = Paginator(clubs,10)
    user = User.objects.get(id=request.user.id)
    clubMember = ClubMember.objects.filter(member=user,position='President')
    context = {
        'club_list': club_list,
        'clubMember_list': clubMember,
    }
    return render(request,"home/club_list.html",context)

def clubView(request):
    isJoined = False
    user = User.objects.get(id=request.user.id)
    club = Club.objects.get(id=request.POST['viewClub'])
    clubMember = ClubMember.objects.filter(club=club,member=user)
    clubImage = ClubImage.objects.filter(club=club)
    if clubMember:
        isJoined = True
    context = {
        'club' : club,
        'isJoined' : isJoined,
        'clubImage': clubImage,
    }
    return render(request,"home/club.html",context)

def editClub(request):
    user = User.objects.get(id=request.user.id)
    selectedClub = Club.objects.get(id=request.POST['editClub'])
    clubImage = ClubImage.objects.filter(club=selectedClub)
    sports = Sport.objects.all().order_by('name')
    universities = University.objects.all().order_by('name')
    form = ImageForm()
    if request.POST.get('name'):
        selectedClub.name = request.POST['name']
        selectedClub.description = request.POST['description']
        selectedClub.sport = Sport.objects.get(id=request.POST['sport'])
        selectedClub.university = University.objects.get(id=request.POST['university'])
        selectedClub.save()

        images = request.FILES.getlist('image')
        for img in images:
            ClubImage.objects.create(club=selectedClub,image=img)

        msg = 'Successfully updated club information'
        context = {
            'msg' : msg,
        }
        return render(request, "home/index.html", context)
    context = {
        'club' : selectedClub,
        'clubImage': clubImage,
        'sports' : sports,
        'universities' : universities,
        'form' : form,
    }
    return render(request,"home/edit_club.html",context)

def joinClub(request):
    user = User.objects.get(id=request.user.id)
    selectedClub = Club.objects.get(id=request.POST['club'])
    newClubMember = ClubMember(
        club = selectedClub,
        member = user,
        position = 'Member',
    )
    newClubMember.save()

    clubs = Club.objects.all().order_by('name')
    club_list = Paginator(clubs,10)
    context = {
        'club_list': club_list,
    }
    return render(request,"home/club_list.html",context)

def createEvent(request):
    msg = None
    success = False
    club_event = False
    user = User.objects.get(id=request.user.id)
    sports = Sport.objects.all().order_by('name')
    states = State.objects.all().order_by('name')
    cities = Cities.objects.all().order_by('name')
    facilities = Facility.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    sponsors = Sponsor.objects.all().order_by('name')
    clubPosition = ClubMember.objects.get(member=user).position
    userClub = ClubMember.objects.filter(member=user,position="President")
    firstClub = userClub[0]
    form = ImageForm()
    if clubPosition != 'Member':
        club_event = True

    if request.method == "POST":
        new_event = Event(
            name = request.POST['name'],
            event_date = request.POST['event_datetime'],
            expiry_date = request.POST['expiry_datetime'],
            sport = Sport.objects.get(id=request.POST['sport']),
            status = 'Open',
            category = request.POST['category'],
            price = request.POST['price'],
        )
        new_event.save()

        if(request.POST.get('PersonalOrClub')=='Personal'):
            new_event.organizer_person = user
        else:
            new_event.organizer_club = Club.objects.get(id=request.POST['club'])

        if(request.POST['sponsor']!=""):
            new_event.sponsor = Sponsor.objects.get(id=request.POST['sponsor'])

        msg = 'Successfully created event'
        context = {
            'msg' : msg,
            'success':success,
        }
        return render(request, "home/index.html", context)
    context = {
        'sports':sports,
        'states' : states,
        'cities' : cities,
        'facilities' : facilities,
        'club_event' : club_event,
        'categories' : categories,
        'sponsors'   : sponsors,
        'form'       : form,
        'userClub'   : userClub,
    }
    return render(request, "home/create_event.html", context)

def eventList(request):
    events = Event.objects.all().order_by('name')
    event_list = Paginator(events,5)
    context = {
        'event_list' : event_list,
    }
    return render(request,"home/event_list.html",context)

def eventView(request):
    user = User.objects.get(id=request.user.id)
    event = Event.objects.get(id=request.POST['viewEvent'])
    eventImage = EventImage.objects.filter(event=event)
    context = {
        'event' : event,
        'eventImage': eventImage,
    }
    return render(request,"home/event.html",context)

def editEvent(request):
    user = User.objects.get(id=request.user.id)
    selectedEvent = Club.objects.get(id=request.POST['editEvent'])
    eventImage = EventImage.objects.filter(club=selectedEvent)
    sports = Sport.objects.all().order_by('name')
    universities = University.objects.all().order_by('name')
    form = ImageForm()
    if request.POST.get('name'):
        selectedEvent.name = request.POST['name']
        selectedEvent.description = request.POST['description']
        selectedEvent.sport = Sport.objects.get(id=request.POST['sport'])
        selectedEvent.university = University.objects.get(id=request.POST['university'])
        selectedEvent.save()

        images = request.FILES.getlist('image')
        for img in images:
            ClubImage.objects.create(club=selectedEvent,image=img)

        msg = 'Successfully updated club information'
        context = {
            'msg' : msg,
        }
        return render(request, "home/index.html", context)
    context = {
        'club' : selectedEvent,
        'clubImage': eventImage,
        'sports' : sports,
        'universities' : universities,
        'form' : form,
    }
    return render(request,"home/edit_club.html",context)