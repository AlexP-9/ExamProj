from django.contrib import admin

from .models import Customer, Guide, Review, Trip, TripGallery, Tag, Difficulty, Schedule

# Register your models here.


admin.site.register(Difficulty)
admin.site.register(Tag)
admin.site.register(Trip)
admin.site.register(TripGallery)
admin.site.register(Review)

admin.site.register(Customer)
admin.site.register(Guide)

admin.site.register(Schedule)