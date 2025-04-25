from django import forms
from django.forms import ClearableFileInput
from .models import Trip, TripGallery

#https://stackoverflow.com/questions/77212709/django-clearablefileinput-does-not-support-uploading-multiple-files-error

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class FormAddTrip(forms.ModelForm):
    class Meta:
        model=Trip
        exclude=[]

class FormAddImages(forms.ModelForm):
    #image=MultipleFileField(label='Select files', required=False)
    picture=MultipleFileField(label='Select files', required=False)
    class Meta:
        model=TripGallery
        fields=("picture",)

