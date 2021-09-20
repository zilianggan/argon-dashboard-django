from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class createClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name','description','sport','university']

class ImageForm(forms.Form):
    # image = forms.ImageField(label="Upload Image",widget=forms.ClearableFileInput(attrs={'multiple':True}))
    class Meta:
        model = ClubImage
        # fields = ['image']

class createEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','event_date','expiry_date','sport','category','status','price','organizer_person','organizer_club','sponsor','facilities']

class ImageForm(forms.Form):
    image = forms.ImageField(label="Upload Image",widget=forms.ClearableFileInput(attrs={'multiple':True}))
    class Meta:
        model = EventImage
        fields = ['image']