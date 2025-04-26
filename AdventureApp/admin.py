from django.contrib import admin

from .models import Trip, TripGallery, Tag, Difficulty

# Register your models here.

admin.site.register(Difficulty)
admin.site.register(Tag)
admin.site.register(Trip)
admin.site.register(TripGallery)