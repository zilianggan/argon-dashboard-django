# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
# from django.contrib.auth.models import User
from ..authentication.models import User

class UserProfile(models.Model):
    class Meta:
        db_table    = 'UserProfile'
        verbose_name_plural    = 'UserProfile'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

# class FriendList(models.Model):

class Sport(models.Model):
    class Meta:
        db_table        = 'Sport'
        verbose_name_plural = 'Sport'
    name    = models.CharField(max_length=100,null=False,blank=False)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    class Meta:
        db_table = 'Category'
        verbose_name_plural = 'Category'
    name    = models.CharField(max_length=100,null=False,blank=False)

    def __str__(self):
        return self.name

class Sponsor(models.Model):
    class Meta:
        db_table            = 'Sponsor'
        verbose_name_plural = 'Sponsor'
    name    = models.TextField()
    contact = models.CharField(max_length=25, blank=True, null=True)

class University(models.Model):
    class Meta:
        db_table            = 'University'
        verbose_name_plural = 'University'
    name        = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Club(models.Model):
    class Meta:
        db_table            = 'Club'
        verbose_name_plural = 'Club'
    name        = models.TextField()
    description = models.TextField()
    sport       = models.ForeignKey(Sport,on_delete=models.CASCADE,blank=False,null=False)
    university  = models.ForeignKey(University,on_delete=models.CASCADE,blank=False,null=False)

    def __str__(self):
        return self.name

class ClubMember(models.Model):
    class Meta:
        db_table        = 'ClubMember'
        verbose_name_plural = 'ClubMember'
    club = models.ForeignKey(Club,on_delete=models.CASCADE,blank=False,null=False)
    member = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)
    position = models.CharField(max_length=100,blank=False,null=False)

class ClubImage(models.Model):
    class Meta:
        db_table        = 'ClubImage'
        verbose_name_plural = 'ClubImage'
    club = models.ForeignKey(Club,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='club_images/',blank=True)

class State(models.Model):
    class Meta:
        db_table = 'State'
        verbose_name_plural = 'State'
    name = models.CharField(max_length=100,blank=False,null=False)

    def __str__(self):
        return self.name

class Cities(models.Model):
    class Meta:
        db_table = 'Cities'
        verbose_name_plural = 'Cities'
    name = models.CharField(max_length=100,blank=False,null=False)
    state = models.ForeignKey(State,on_delete=models.CASCADE,blank=False,null=False)

    def __str__(self):
        return self.name

class Facility(models.Model):
    class Meta:
        db_table            = 'Facility'
        verbose_name_plural = 'Facility'
    name     = models.CharField(max_length=100,blank=False,null=False)
    address = models.TextField()
    city     = models.ForeignKey(Cities,on_delete=models.CASCADE,blank=False,null=False)
    postcode = models.IntegerField(blank=False,null=False)
    sport    = models.ForeignKey(Sport,on_delete=models.CASCADE,blank=False,null=False)

class Event(models.Model):
    class Meta:
        db_table            = 'Event'
        verbose_name_plural = 'Event'
    name        = models.TextField()
    event_date  = models.DateTimeField()
    expiry_date  = models.DateTimeField()
    sport       = models.ForeignKey(Sport,on_delete=models.CASCADE,blank=False,null=False)
    category    = models.CharField(max_length=100,blank=False,null=False)
    status      = models.CharField(max_length=50,blank=False,null=False)
    price       = models.IntegerField()
    organizer_person = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    organizer_club   = models.ForeignKey(Club,on_delete=models.CASCADE,blank=True,null=True)
    sponsor     = models.ForeignKey(Sponsor,on_delete=models.CASCADE,blank=True,null=True)
    facilities  = models.ForeignKey(Facility,on_delete=models.CASCADE,blank=True,null=True)

class EventImage(models.Model):
    class Meta:
        db_table        = 'EventImage'
        verbose_name_plural = 'EventImage'
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/')

class EventMember(models.Model):
    class Meta:
        db_table        = 'EventMember'
        verbose_name_plural = 'EventMember'
    event = models.ForeignKey(Event,on_delete=models.CASCADE,blank=False,null=False)
    member = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)

class Review(models.Model):
    class Meta:
        db_table = 'Review'
        verbose_name_plural = 'Review'
    star_rate = models.IntegerField()
    comment   = models.TextField()