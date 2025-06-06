from django.db import models
from django.core.validators import RegexValidator, MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(
        max_length=32,
        validators=[
            RegexValidator(regex=r"^\+?1?\d{9,15}$", #https://www.geeksforgeeks.org/properly-store-and-validate-phone-numbers-in-django-models/
                           message="Invalid phone number format!")
        ],
        unique=True)
    newsletter=models.BooleanField()
    def __str__(self):
        return(f"{self.user.first_name} {self.user.last_name} ({self.user.username})")
    class Meta:
    	verbose_name_plural="Customers"

class Tag(models.Model):
    name=models.CharField(max_length=255, unique=True)
    def __str__(self):
        return(f"{self.name}")

class Difficulty(models.Model):
    name=models.CharField(max_length=255, unique=True)
    description=models.TextField()
    def __str__(self):
        return(f"{self.name}")
    class Meta:
    	verbose_name_plural="Difficulties"

class Trip(models.Model):
    title=models.CharField(max_length=255, unique=True)
    description=models.TextField()
    tags=models.ManyToManyField(Tag)
    difficulty=models.ForeignKey(Difficulty, on_delete=models.RESTRICT)    #Or models.SET_NULL or models.CASCADE
    def __str__(self):
        return(f"{self.title}")

class TripGallery(models.Model):
    picture=models.ImageField(upload_to="TripImages/")
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE)
    def __str__(self):
        return(f"{self.trip.title} - {self.picture.name}")
    class Meta:
    	verbose_name_plural="Media files"

class Guide(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255, unique=True)
    portrait=models.ImageField(upload_to="GuidePics/", blank=True, null=True)
    description=models.TextField()

    phone=models.CharField(
        max_length=32,
        validators=[
            RegexValidator(regex=r"^\+?1?\d{9,15}$", #https://www.geeksforgeeks.org/properly-store-and-validate-phone-numbers-in-django-models/
                           message="Invalid phone number format!")                   
        ]
        )

    def __str__(self):
        return(f"{self.name}")

class Schedule(models.Model):
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE)
    start=models.DateTimeField()
    end=models.DateTimeField()
    price=models.DecimalField(max_digits=12,decimal_places=2)
    maxattendants=models.IntegerField(verbose_name="Max. attendants")
    attendants=models.ManyToManyField(User, blank=True, related_name="schedules")
    guides=models.ManyToManyField(Guide)

    class Meta:
        #The starting date can't be >= than the ending date
        constraints=[
            models.CheckConstraint(
                check=models.Q(
                    start__lte=models.F("end")
                ),
                name="starts_earlier_than_finishes",
                violation_error_message="Trip should start first before it ends!"
            )
        ]

    def __str__(self):
        return(f"{self.trip.title} - From {self.start} to {self.end}, {self.attendants.count()} attendants")
        

class Review(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    revtrip=models.ForeignKey(Trip, null=True, on_delete=models.SET_NULL)
    rating=models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(10)
    ])
    revtitle=models.CharField(max_length=255)
    comment=models.TextField()
    date_created=models.DateTimeField(auto_now_add=True)
    date_edited=models.DateTimeField(auto_now=True)
    
    #https://stackoverflow.com/questions/58115738/realizing-rating-in-django
    class Meta:
        #Users can only have one review per trip
        constraints=[
            models.UniqueConstraint(fields=["customer","revtrip"],name="unique_rating")
        ]

    def __str__(self):
        return(f"{self.revtrip}: {self.rating}/{self.revtitle}/{self.customer}")
