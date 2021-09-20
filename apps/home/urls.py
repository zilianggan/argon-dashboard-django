# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import include, path, re_path
from apps.home import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('edit-profile',editProfile,name='edit-profile'),
    path('upload-profile-picture',uploadProfilePic,name='upload-profile-picture'),
    path('create-club', createClub, name='create-club'),
    path('club-list', clubList, name='club-list'),
    path('club',clubView,name='club'),
    path('edit-club',editClub,name='edit-club'),
    path('join-club',joinClub,name='join-club'),
    path('create-event', createEvent, name='create-event'),
    path('event-list',eventList,name='event-list'),
    path('event',eventView,name='event'),
    path('edit-event', editEvent, name='edit-event'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)