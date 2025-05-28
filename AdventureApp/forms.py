from django import forms
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput
from .models import Schedule, Trip, TripGallery, Customer

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


class FormRegister(forms.ModelForm):
    class Meta:
        model=Customer
        exclude=[]