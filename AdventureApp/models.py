from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Customer(AbstractUser):
    phone=models.CharField(
        max_length=32,
        validators=[
            RegexValidator(regex="^\+?1?\d{9,15}$", #https://www.geeksforgeeks.org/properly-store-and-validate-phone-numbers-in-django-models/
                           message="Invalid phone number format!")
        ])


class Tag(models.Model):
    name=models.CharField(max_length=255)

class Difficulty(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()

class Trip(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    tags=models.ManyToManyField(Tag)
    difficulty=models.ForeignKey(Difficulty, on_delete=models.RESTRICT)    #Or models.SET_NULL or models.CASCADE
    #difficulty=models.IntegerField(choices=[(0,"Very easy"),()])

class TripGallery(models.Model):
    picture=models.ImageField(upload_to="TripMedia/")
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE)
    #^Should this be able to be NULL?^
    #What happens after deletion, do files stay?

class Guide(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    phone=models.CharField(
        max_length=32,
        validators=[
            RegexValidator(regex="^\+?1?\d{9,15}$", #https://www.geeksforgeeks.org/properly-store-and-validate-phone-numbers-in-django-models/
                           message="Invalid phone number format!")
        ])

class Schedule(models.Model):
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE)
    start=models.DateTimeField()
    end=models.DateTimeField()
    price=models.DecimalField(max_digits=12,decimal_places=2)
    maxattendants=models.IntegerField()
    attendants=models.ManyToManyField(Customer)
    guides=models.ManyToManyField(Guide)

class Review(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    revtrip=models.ForeignKey(Trip, null=True, on_delete=models.SET_NULL)
    #^Should this be able to be NULL?^
    rating=models.IntegerField()
    revtitle=models.CharField(max_length=255)
    comment=models.TextField()
