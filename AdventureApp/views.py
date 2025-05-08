from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from .forms import FormAddTrip, FormAddImages
from .models import Review, Trip, TripGallery

# Create your views here.
"""
#Registration, Login, Logout
"""
def view_login(request):
    if(request.method=="POST"):
        uname=request.POST.get("username")
        passw=request.POST.get("password")
        user=authenticate(request,username=uname,password=passw)
        if user:    #if user is not None:
            login(request,user)
            return redirect(request.GET.get("next",""))
        messages.add_message(request, messages.WARNING, "Incorrect password!")
        return render(request,"LogIn.html",{
            "username":uname            
        })
    return render(request, "LogIn.html")

def view_logout(request):
    logout(request)
    return redirect("")

def view_register(request):
    return render()

"""
#Trip views (all, individual, etc.)
"""
def view_mainpage(request):
    tripsdb=Trip.objects.all
    return render(request, "MainPage.html",
                  {
                      "trips":tripsdb
                  })

def view_trip(request, tid):
    tripdb=get_object_or_404(Trip,id=tid)
    picsdb=TripGallery.objects.filter(trip__id=tid)
    reviewsdb=Review.objects.filter(revtrip=tid)
    return render(request, "TripPage.html",
                  {
                      "tripobj":tripdb,
                      "picobjs":picsdb,
                      "reviews":reviewsdb,
                  })

def view_all_trips(request):
    all_trips = Trip.objects.all()
    return render(request, "AllTrips.html", {
        "trips": all_trips
    })


"""
#Administrational views
"""
#@staff_member_required
def view_managing_panel(request):
    return render(request,"ManagingPanel.html")

#@staff_member_required
def view_add_trip(request):
    formtrip=FormAddTrip()
    formim=FormAddImages()
    if(request.method=="POST"):
        formtrip=FormAddTrip()
        formim=FormAddImages()
        uplimages=request.FILES.getlist("picture")
        print("Post")
        print(request.FILES)
        for i in uplimages:
            print(i)
    
    return render(request,"AdminAddTrip.html",{
        "FormTrip":formtrip,
        "FormIm":formim
    })

"""
#Debug
"""
def view_debug(request):
    return render(request,"Debug.html")
