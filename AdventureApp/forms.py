from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.forms import ClearableFileInput
from .models import Schedule, Trip, TripGallery, Customer, Review, Guide

#https://stackoverflow.com/questions/77212709/django-clearablefileinput-does-not-support-uploading-multiple-files-error


class FormAddTrip(forms.ModelForm):
    class Meta:
        model=Trip
        fields="__all__"

class FormAddImage(forms.ModelForm):
    class Meta:
        model=TripGallery
        fields=("picture",)


#https://stackoverflow.com/questions/50214773/type-datetime-local-in-django-form
class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"
 
class DateTimeLocalField(forms.DateTimeField):
    # Set DATETIME_INPUT_FORMATS here because, if USE_L10N 
    # is True, the locale-dictated format will be applied 
    # instead of settings.DATETIME_INPUT_FORMATS.
    # See also: 
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Date_and_time_formats
     
    input_formats = [
        "%Y-%m-%dT%H:%M:%S", 
        "%Y-%m-%dT%H:%M:%S.%f", 
        "%Y-%m-%dT%H:%M",
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")

class FormAddSchedule(forms.ModelForm):
    start=DateTimeLocalField()
    end=DateTimeLocalField()
    class Meta:
        model=Schedule
        exclude=["attendants",]
    #I will check it in the view. It's easier to exclude the instance by ID there.
    """
    def clean(self):
        cleandata=self.cleaned_data
        overlaps=set(Schedule.objects.filter(
                start__lte=cleandata["end"],
                end__gte=cleandata["start"],
                guides__in=cleandata["guides"]
            ).exclude(id=cleandata["id"]))
        if(overlaps):
            raise ValidationError(f"There is an overlap with existing schedule! ({len(overlaps)} conflicts): "+";\n".join(str(o) for o in overlaps))
        return cleandata
    """


""""
class FormRegister(forms.Form):
    username=forms.CharField(max_length=255)
    pwd=forms.PasswordInput()
    pwd_check=forms.PasswordInput()
    phone=forms.CharField(
        max_length=32,
        validators=[
            RegexValidator(regex=r"^\+?1?\d{9,15}$", #https://www.geeksforgeeks.org/properly-store-and-validate-phone-numbers-in-django-models/
                           message="Invalid phone number format!")
        ])
    newsletter=forms.BooleanField(required=False)
    def clean(self):
        super(FormRegister, self).clean()
        print(self.cleaned_data)
        if(self.cleaned_data.get("password")!=self.cleaned_data.get("password_check")):
            self._errors["password"]=self.error_class(["Passwords don't match!"])
        return self.cleaned_data
"""

class FormRegister(UserCreationForm):
    phone=forms.CharField(
        max_length=32,
        validators=[
            RegexValidator(regex=r"^\+?1?\d{9,15}$", #https://www.geeksforgeeks.org/properly-store-and-validate-phone-numbers-in-django-models/
                           message="Invalid phone number format!")
        ])
    #fullname=forms.CharField(max_length=255)
    newsletter=forms.BooleanField(required=False)
    class Meta:
        model=User
        fields=["username", "first_name", "last_name", "password1", "password2"]

    


class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        exclude=["date_created","date_edited","customer","revtrip"]



#################################################################
class FormGuide(forms.ModelForm):
    class Meta:
        model=Guide
        fields=["name","email","phone","description","portrait"]
